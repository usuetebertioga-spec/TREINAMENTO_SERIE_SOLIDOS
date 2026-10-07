import streamlit as st
import streamlit.components.v1 as components
from fpdf import FPDF
from datetime import datetime
import os
import base64

# Configuração da Página
st.set_page_config(
    page_title="Tecwater Systems - Treinamento SST, SSV e SF",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Base de Usuários Cadastrados
USUARIOS = {
    "genilson moura barros": {
        "senha": "GMB#2026",
        "nome": "Genilson Moura Barros",
        "funcao": "Supervisor Técnico",
        "unidade": "ETEB SESC Bertioga"
    },
    "operador02": {
        "senha": "Op2_ETEB#2026",
        "nome": "Operador ETEB 02",
        "funcao": "Técnico de Operação",
        "unidade": "ETEB SESC Bertioga"
    }
}

# Inicialização do Estado da Sessão
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario_atual" not in st.session_state:
    st.session_state.usuario_atual = None
if "nota_quiz" not in st.session_state:
    st.session_state.nota_quiz = None
if "aprovado" not in st.session_state:
    st.session_state.aprovado = False

# Função para converter imagem em Base64 para HTML
def carregar_imagem_base64(caminho):
    if os.path.exists(caminho):
        with open(caminho, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded_string}"
    return None

# Função para Gerar o Arquivo PDF do Certificado com FPDF
def gerar_pdf_certificado(nome, funcao, unidade, nota):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    
    # Moldura Dupla do Certificado
    pdf.set_line_width(1.2)
    pdf.rect(8, 8, 281, 194)
    pdf.set_line_width(0.4)
    pdf.rect(10, 10, 277, 190)
    
    # Inserir Logo no PDF se existir no diretório
    if os.path.exists("logo.jpg"):
        pdf.image("logo.jpg", x=123, y=16, w=50)
        pdf.ln(30)
    else:
        pdf.ln(12)
        pdf.set_font("Arial", 'B', 22)
        pdf.cell(0, 12, "TECWATER SYSTEMS", ln=True, align='C')
        
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 10, "COMPROVANTE DE CAPACITACAO OPERACIONAL", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 6, f"ESTACAO DE TRATAMENTO DE EFLUENTES ({unidade.upper()})", ln=True, align='C')
    pdf.ln(12)
    
    # Texto Oficial do Certificado
    pdf.set_font("Arial", '', 13)
    texto = (
        f"Certificamos para os devidos fins de conformidade operacional que o(a) colaborador(a) "
        f"{nome}, na funcao de {funcao}, concluiu com exito o treinamento teorico-pratico referente "
        f"ao Procedimento Operacional Padrao (POP) de Analise de Ensaios de SST, SSV e SF."
    )
    pdf.multi_cell(0, 7, texto, align='C')
    pdf.ln(10)
    
    # Dados de Conclusão e Atendimento Legal
    data_hoje = datetime.now().strftime("%d/%m/%Y as %H:%M")
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 6, f"Aproveitamento Final na Avaliacao: {nota:.0f}% (Aprovado)", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 6, "Atendimento Legal: Decreto Estadual SP nº 8.468/1976 - Artigo 18", ln=True, align='C')
    pdf.cell(0, 6, f"Data de Conclusao e Emissao: {data_hoje}", ln=True, align='C')
    pdf.ln(20)
    
    # Assinatura
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 5, "______________________________________________________", ln=True, align='C')
    pdf.cell(0, 5, f"{nome} - Registro e Ciente Digital via Plataforma", ln=True, align='C')
    
    nome_arquivo = f"Certificado_{nome.replace(' ', '_')}.pdf"
    pdf.output(nome_arquivo)
    return nome_arquivo

# --- TELA DE LOGIN ---
if not st.session_state.autenticado:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        logo_base64 = carregar_imagem_base64("logo.jpg")
        if logo_base64:
            st.markdown(f"<div style='text-align:center;'><img src='{logo_base64}' width='180'></div>", unsafe_allow_html=True)
        
        st.markdown("<h2 style='text-align: center; color: #0284c7;'>Tecwater Systems</h2>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>Identificação do Colaborador - ETEB SESC Bertioga</h4>", unsafe_allow_html=True)

        with st.form("login_form"):
            usuario_input = st.text_input("Usuário / Matrícula").strip().lower()
            senha_input = st.text_input("Senha Individual", type="password")
            btn_entrar = st.form_submit_button("Entrar no Treinamento", use_container_width=True)

            if btn_entrar:
                if usuario_input in USUARIOS and USUARIOS[usuario_input]["senha"] == senha_input:
                    st.session_state.autenticado = True
                    st.session_state.usuario_atual = USUARIOS[usuario_input]
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("Usuário ou senha individual incorretos.")

# --- ÁREA LOGADA ---
else:
    usr = st.session_state.usuario_atual

    # Barra Lateral
    with st.sidebar:
        logo_base64 = carregar_imagem_base64("logo.jpg")
        if logo_base64:
            st.markdown(f"<div style='text-align:center;'><img src='{logo_base64}' width='160'></div>", unsafe_allow_html=True)
        st.title("Tecwater Systems")
        st.write(f"👤 **Colaborador:** {usr['nome']}")
        st.write(f"💼 **Função:** {usr['funcao']}")
        st.write(f"🏢 **Unidade:** {usr['unidade']}")
        st.divider()

        menu = st.radio(
            "Navegação do Módulo:",
            ["📖 Módulo de Estudo (POP)", "🧮 Calculadora de Parâmetros", "📝 Avaliação de Conhecimento (Quiz)", "📜 Comprovante de Conclusão"]
        )

        st.divider()
        st.markdown("### ⚖️ Legislação Ambiental")
        st.link_button("🌐 Consultar Decreto SP 8.468/1976", "https://www.al.sp.gov.br/norma/51080", use_container_width=True)

        if st.button("🚪 Sair / Trocar Usuário", use_container_width=True):
            st.session_state.autenticado = False
            st.session_state.usuario_atual = None
            st.rerun()

    # --- ABA 1: MÓDULO DE ESTUDO (POP OFICIAL COMPLETO) ---
    if menu == "📖 Módulo de Estudo (POP)":
        st.header("📖 Procedimento Operacional Padrão (POP)")
        st.caption("Documento Oficial Tecwater Systems - Análise de Ensaios de SST, SSV e SF")

        tab1, tab2, tab3, tab4 = st.tabs([
            "📄 I - IV. Diretrizes Oficiais", 
            "🧪 V. Análise SST (5.1 a 5.11)", 
            "🔥 V. Análise SSV/SF (5.12 a 5.22)", 
            "🤿 VI - VIII. Segurança & Ref."
        ])

        with tab1:
            st.subheader("TÍTULO: Análise de Ensaios de SST, SSV e SF")
            st.info("""
            **Elaborado por:** ____________________  
            **Revisado por:** ____________________  
            **Aprovado por:** ____________________  
            **Unidade:** SESC BERTIOGA | **Estado / País:** SÃO PAULO / BRASIL
            """)

            st.markdown("### I. OBJETIVO")
            st.write("""
            Definir metodologia para a realização de análises de SST (Sólidos Suspensos Totais), SSV (Sólidos Suspensos Voláteis) e SF (Sólidos Fixos) do efluente e/ou lodo biológico no sistema de tratamento de efluentes biológicos da ETEB, garantindo o tratamento adequado do efluente sanitário gerado na unidade do SESC Bertioga.
            """)

            st.markdown("### II. ALCANCE")
            st.write("""
            Este procedimento aplica-se à operação da Estação de Tratamento de Efluentes Biológicos (ETEB) da unidade do SESC Bertioga.
            """)

            st.markdown("### III. RESPONSABILIDADES")
            st.markdown("""
            **3.1 Meio Ambiente:**
            * Coordenar as atividades da empresa responsável pela operação da ETEB.
            * Analisar o desempenho da ETEB, considerando todas as informações geradas do controle de tratamento dos efluentes clarificado, incluindo requisitos legais.
            * Definir os controles necessários ao atendimento dos parâmetros de qualidade final dos efluentes tratados, determinados pela Legislação Ambiental de acordo com o **Decreto 8.468 de 1976 – Artigo 18**, para o lançamento no corpo receptor (Rio Itapanhaú).
            * Manter os registros de monitoramento dos parâmetros de controle da ETEB.
            * Tratar junto à equipe de Manutenção quanto às demandas por manutenção de equipamentos e à Equipe do SESC Bertioga quanto à manutenção das instalações e melhorias na ETEB.

            **3.2 Empresa Responsável pela Operação da ETEB:**
            * Supervisionar a operação da ETEB para a realização do tratamento dos efluentes operando os equipamentos e instalações na unidade do SESC Bertioga.
            * Fazer os controles dos parâmetros de entrada e saída de efluentes tratados na ETEB, incluindo as análises químicas para verificação de conformidade legal de acordo com o Decreto 8.468 de 1976 – Artigo 18.
            * Tratar junto à Equipe do SESC Bertioga, as necessidades de solução de problemas nos equipamentos.
            * Apresentar os registros de operação da unidade aos responsáveis do SESC Bertioga.
            * Garantir o cumprimento do plano de manutenção preventiva nas instalações da ETEB.

            **3.3 Operadores da ETEB:**
            * Cabe à operação executar, de forma adequada, a realização das análises dos ensaios de SST (Sólidos Suspensos Totais), SSV (Sólidos Suspensos Voláteis) e SF (Sólidos Fixos), seguindo rigorosamente este procedimento, que visa estabelecer padrões e técnicas para se obter confiabilidade e precisão nos resultados obtidos através das análises realizadas no laboratório.
            """)

            st.markdown("### IV. GENERALIDADES")
            st.write("""
            Cumprir rigorosamente este procedimento de análise de SST (Sólidos Suspensos Totais), SSV (Sólidos Suspensos Voláteis) e SF (Sólidos Fixos) para se obter um resultado de confiabilidade e com precisão a fim de determinar a necessidade de realizar o processo de desidratação do lodo biológico.
            """)

        with tab2:
            st.subheader("V. DESCRIÇÃO DO PROCEDIMENTO - PARTE 1 (SST)")
            st.markdown("""
            **5.1** Para analisarmos a concentração de SST (Sólidos Suspensos Totais), deve-se coletar amostra do efluente do ponto a ser analisado mediante à necessidade operacional;

            **5.2** Identificar o papel filtro com a respectiva amostra a ser analisada;

            **5.3** Verificar o nível da balança analítica para que não ocorra erro na pesagem do mesmo. Se houver a necessidade, nivelar a balança analítica;

            **5.4** Ligar a balança analítica no botão "LIGA / DESLIGA";

            **5.5** Tarar papel filtro, utilizando-se da balança analítica com 3 casas decimais, anotando o peso tarado dos mesmos;

            **5.6** Montar sistema de vácuo com Kitassato, Funil de Buckner e Compressor à Vácuo;

            **5.7** Colocar papel filtro dentro do Funil de Buckner, ligar o compressor à vácuo e adicionar 10 ml da amostra, dosando com pipeta graduada ou volumétrica, sobre o papel filtro espalhando o efluente lentamente a fim de filtrar de forma rigorosa;

            **5.8** Finalizado a filtração, colocar o papel filtro com a amostra filtrada na Estufa à 105°C por 1 (uma) hora;

            **5.9** Após o tempo descrito acima, retirar o papel filtro com a pinça metálica da Estufa e colocá-lo no Dessecador para o resfriamento;

            **5.10** Depois de 1 (uma) hora, retirar o papel filtro do Dessecador e realizar a pesagem do mesmo;

            **5.11** Para obtermos o resultado do SST (Sólidos Suspensos Totais), subtrair o peso do papel filtro após a análise com o peso do papel filtro tarado e multiplicar o resultado obtido por 1000 encontrando o valor em miligramas por litro.  
            * **Fórmula:** `SST (mg/L) = (Peso do filtro com amostra - tara do filtro) × 1000`
            """)

        with tab3:
            st.subheader("V. DESCRIÇÃO DO PROCEDIMENTO - PARTE 2 (SSV e SF)")
            st.markdown("""
            **5.12** Para encontrarmos o SSV (Sólidos Suspensos Voláteis), deve-se coletar amostra do efluente do ponto a ser analisado mediante à necessidade operacional;

            **5.13** Identificar o cadinho com a respectiva amostra a ser analisada;

            **5.14** Verificar o nível da balança analítica para que não ocorra erro na pesagem do mesmo. Se houver a necessidade, nivelar a balança analítica;

            **5.15** Ligar a balança analítica no botão "LIGA / DESLIGA";

            **5.16** Tarar o cadinho, utilizando-se da balança analítica com 3 casas decimais, anotando o peso tarado;

            **5.17** Dosar 10 ml da amostra do efluente no cadinho utilizando pipeta graduada ou volumétrica pertencentes a um dos tanques de aeração já mencionado acima;

            **5.18** Para ligar a Mufla, deve-se verificar se o equipamento está ligada na tomada 220V. Girar a chave seletora para "Acima 400 °C" e verificar se o Set-Point está programado para 550 °C apertando o PGM, caso a programação estiver fora do recomendado para esta análise, acertar o Set-Point apertando os botões ↑ ↓, conforme a necessidade do processo;

            **5.19** Colocar o cadinho dentro Mufla à 550°C ± 50°C por 1 horas para processo de calcinação, utilizando a luva apropriada para altas temperaturas;

            **5.20** Após o processo de calcinação e secagem, descansar a(s) amostra(s) do cadinho, no dessecador aguardando o processo de resfriamento do mesmo;

            **5.21** Pesar cadinho e relacionar resultados com a tara já obtida, subtraindo o peso do cadinho mais amostra com o peso da tara do cadinho, multiplicando o resultado obtido por 100 encontrando o valor em miligramas por litro.  
            * **Fórmula:** `SF (mg/L) = (peso do cadinho com amostra - tara do cadinho) × 1000`

            **5.22** Para calcular o SSV (Sólidos Suspensos Voláteis), análise necessária para calcular o IVL (Índice Volumétrico do Lodo), utilizar a fórmula:  
            * **Fórmula:** `SST = SSV + SF`
            """)

        with tab4:
            st.subheader("VI. MEIO AMBIENTE E SEGURANÇA")
            st.warning("""
            Todas as etapas de análises de SST (Sólidos Suspensos Totais), SSV (Sólidos Suspensos Voláteis) e SF (Sólidos Fixos) são necessárias para garantir a eficiência na realização de análises e obter confiabilidade e precisão nos resultados. 

            A análise deverá ser realizada com a utilização correta dos EPI's recomendados:
            * 👓 **Óculos de Segurança**
            * 🧤 **Luva de Procedimento**
            * 🥼 **Avental Operacional**
            * 🛡️ **Luva de Alta Temperatura** (para manuseio na Mufla)
            * Outros procedimentos de segurança aplicáveis.
            """)

            st.markdown("### VII. REFERÊNCIAS")
            st.write("Manual de Operação da ETEB.")

            st.markdown("### VIII. REGISTROS")
            st.write("Não se aplica.")

    # --- ABA 2: CALCULADORA DE PARÂMETROS ---
    elif menu == "🧮 Calculadora de Parâmetros":
        st.header("🧮 Calculadora de Parâmetros Laboratoriais")
        st.caption("Insira os dados da análise para calcular SST, SF e SSV automaticamente.")

        col_a, col_b = st.columns(2)
        with col_a:
            vol = st.number_input("Volume da Amostra (mL)", value=10.0, step=1.0)
            m1 = st.number_input("Tara do Filtro m1 (g)", value=0.085, format="%.4f")
            m2 = st.number_input("Massa Filtro + Amostra Seca 105°C m2 (g)", value=0.092, format="%.4f")

        with col_b:
            m_cad = st.number_input("Tara do Cadinho (g)", value=15.200, format="%.4f")
            m3 = st.number_input("Massa Cadinho + Filtro Calcinado 550°C m3 (g)", value=15.202, format="%.4f")

        if st.button("Calcular Resultados", use_container_width=True):
            if vol > 0:
                sst = ((m2 - m1) * 1000)
                sf = ((m3 - m_cad) * 1000)
                ssv = sst - sf

                st.success(f"**SST (Sólidos Suspensos Totais):** {sst:.2f} mg/L")
                st.info(f"**SF (Sólidos Fixos):** {sf:.2f} mg/L")
                st.info(f"**SSV (Sólidos Suspensos Voláteis):** {ssv:.2f} mg/L")
            else:
                st.error("O volume da amostra deve ser maior que zero.")

    # --- ABA 3: AVALIAÇÃO DE CONHECIMENTO (QUIZ) ---
    elif menu == "📝 Avaliação de Conhecimento (Quiz)":
        st.header("📝 Avaliação Teórica e Operacional (10 Questões)")
        st.write("Responda às questões. A pontuação mínima para aprovação é de **50%** (5 acertos).")

        with st.form("quiz_form"):
            q1 = st.radio("1. Qual legislação estadual de SP regulamenta os limites de efluentes da ETEB?", 
                          ["Decreto Estadual SP nº 8.468/1976 – Artigo 18", "Portaria GM/MS nº 888", "Resolução CONAMA 357"])
            q2 = st.radio("2. Tempo e temperatura de secagem do filtro na Estufa para SST?", 
                          ["105°C por 1 hora", "80°C por 30 minutos", "550°C por 1 hora"])
            q3 = st.radio("3. Equipamento e temperatura para calcinação de SSV e SF?", 
                          ["Mufla a 550°C ± 50°C por 1 hora", "Estufa a 105°C", "Dessecador"])
            q4 = st.radio("4. Onde as amostras resfriam sem absorver umidade?", 
                          ["Dentro do Dessecador por 1 hora", "Na bancada aberta", "No freezer"])
            q5 = st.radio("5. Qual a precisão da balança analítica utilizada?", 
                          ["Balança com precisão de 3 casas decimais", "Balança comercial de 1 casa", "Sem calibração"])
            q6 = st.radio("6. Qual a fórmula oficial do SST em mg/L conforme o POP?", 
                          ["SST (mg/L) = (Peso do filtro com amostra - tara do filtro) × 1000", "SST = m2 / m1", "SST = m1 + m2"])
            q7 = st.radio("7. Como se obtém a relação para calcular o SSV?", 
                          ["SST = SSV + SF", "SSV = SST + SF", "SSV = SF / 2"])
            q8 = st.radio("8. EPI obrigatório ao manusear materiais na Mufla a 550°C?", 
                          ["Luva de alta temperatura", "Luvas de nitrilo", "Sem EPI"])
            q9 = st.radio("9. Volume padrão da alíquota filtrada na rotina da ETEB?", 
                          ["10 ml", "100 ml", "1000 ml"])
            q10 = st.radio("10. Função do compressor e frasco Kitassato no ensaio?", 
                          ["Montar sistema de vácuo para filtração", "Aquecer a água", "Medir o pH"])

            btn_quiz = st.form_submit_button("Finalizar Avaliação e Calcular Nota", use_container_width=True)

            if btn_quiz:
                acertos = 0
                if q1 == "Decreto Estadual SP nº 8.468/1976 – Artigo 18": acertos += 1
                if q2 == "105°C por 1 hora": acertos += 1
                if q3 == "Mufla a 550°C ± 50°C por 1 hora": acertos += 1
                if q4 == "Dentro do Dessecador por 1 hora": acertos += 1
                if q5 == "Balança com precisão de 3 casas decimais": acertos += 1
                if q6 == "SST (mg/L) = (Peso do filtro com amostra - tara do filtro) × 1000": acertos += 1
                if q7 == "SST = SSV + SF": acertos += 1
                if q8 == "Luva de alta temperatura": acertos += 1
                if q9 == "10 ml": acertos += 1
                if q10 == "Montar sistema de vácuo para filtração": acertos += 1

                nota = (acertos / 10) * 100
                st.session_state.nota_quiz = nota
                st.session_state.aprovado = nota >= 50

                if st.session_state.aprovado:
                    st.success(f"🎉 Parabéns, {usr['nome']}! Você acertou {acertos} de 10 perguntas (Nota {nota:.0f}%) e foi APROVADO!")
                    st.balloons()
                else:
                    st.error(f"Sua nota foi {nota:.0f}% ({acertos} acertos). A nota mínima é 50%. Tente novamente.")

    # --- ABA 4: COMPROVANTE DE CONCLUSÃO ---
    elif menu == "📜 Comprovante de Conclusão":
        st.header("📜 Comprovante de Capacitação Operacional")

        if st.session_state.aprovado:
            nota_obtida = st.session_state.nota_quiz if st.session_state.nota_quiz is not None else 100
            data_hoje = datetime.now().strftime("%d/%m/%Y")
            logo_src = carregar_imagem_base64("logo.jpg") or ""

            # Visual do Comprovante em HTML
            html_cert = f"""
            <div style="border: 2px solid #0284c7; border-radius: 12px; padding: 40px; background-color: #ffffff; color: #0f172a; max-width: 850px; margin: 0 auto; font-family: 'Arial', sans-serif;">
                <div style="text-align: center; margin-bottom: 20px;">
                    {"<img src='" + logo_src + "' width='140' style='margin-bottom:10px;'><br>" if logo_src else ""}
                    <h2 style="margin: 0; color: #0284c7; letter-spacing: 1px;">TECWATER SYSTEMS</h2>
                    <h3 style="margin: 10px 0 0 0; color: #1e293b;">COMPROVANTE DE CAPACITAÇÃO OPERACIONAL</h3>
                    <p style="margin: 5px 0 0 0; color: #64748b; font-size: 14px;">ETEB SESC BERTIOGA</p>
                </div>
                <hr style="border: none; border-top: 1px solid #cbd5e1; margin: 25px 0;">
                <p style="font-size: 16px; line-height: 1.8; text-align: center; color: #334155;">
                    Certificamos que o(a) operador(a) <b>{usr['nome']}</b> concluiu com êxito o treinamento teórico-prático referente ao procedimento de <b>Análise de SST, SSV e SF</b>, obtendo aproveitamento de <b>{nota_obtida:.0f}%</b> na avaliação.
                </p>
                <div style="display: flex; justify-content: space-around; margin-top: 40px; text-align: center;">
                    <div>
                        <p style="margin: 0; font-size: 14px; font-weight: bold; color: #475569;">Atendimento Legal:</p>
                        <p style="margin: 4px 0 0 0; font-size: 14px; color: #64748b;">Decreto Estadual nº 8.468/1976 - Artigo 18</p>
                    </div>
                    <div>
                        <p style="margin: 0; font-size: 14px; font-weight: bold; color: #475569;">Data da Conclusão:</p>
                        <p style="margin: 4px 0 0 0; font-size: 14px; color: #64748b;">{data_hoje}</p>
                    </div>
                </div>
                <hr style="border: none; border-top: 1px solid #cbd5e1; margin: 30px 0 15px 0;">
                <p style="font-size: 11px; text-align: center; color: #94a3b8; margin: 0;">REGISTRO AUDITÁVEL TECWATER SYSTEMS | PLATAFORMA DE TREINAMENTO</p>
            </div>
            """
            st.markdown(html_cert, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            col_pdf, col_print = st.columns([1, 1])
            
            with col_pdf:
                arquivo_pdf = gerar_pdf_certificado(usr['nome'], usr['funcao'], usr['unidade'], nota_obtida)
                
                with open(arquivo_pdf, "rb") as pdf_file:
                    st.download_button(
                        label="📥 Baixar Comprovante em PDF",
                        data=pdf_file,
                        file_name=arquivo_pdf,
                        mime="application/pdf",
                        use_container_width=True
                    )

            with col_print:
                components.html(
                    """
                    <button onclick="window.parent.print()" style="width:100%; height:45px; background-color:#0284c7; color:white; border:none; border-radius:8px; font-weight:bold; font-size:15px; cursor:pointer;">
                        🖨️ Imprimir / Salvar Registro no Navegador
                    </button>
                    """,
                    height=50
                )
        else:
            st.warning("⚠️ Você precisa responder o quiz e obter no mínimo 50% de aprovação para liberar o Comprovante.")