import streamlit as st
import textwrap

from api_client import ask_backend


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="RAG Study Assistant",
    page_icon="📚",
    layout="wide",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   GLOBAL
============================================================ */

.stApp {
    background:
        radial-gradient(
            circle at 8% 8%,
            rgba(108, 99, 255, 0.14),
            transparent 28%
        ),
        radial-gradient(
            circle at 92% 18%,
            rgba(0, 194, 255, 0.12),
            transparent 30%
        ),
        radial-gradient(
            circle at 82% 88%,
            rgba(255, 107, 107, 0.10),
            transparent 28%
        ),
        #f7f8fc;
}


.block-container {
    max-width: 1120px;
    padding-top: 2rem;
    padding-bottom: 5rem;
}


html,
body,
[class*="css"] {
    color: #1f2937;
}


h1,
h2,
h3 {
    color: #1f2937;
}


a {
    color: #6c63ff;
}


::selection {
    background: rgba(108, 99, 255, 0.22);
}



/* ============================================================
   HERO
============================================================ */

.hero-container {
    position: relative;
    overflow: hidden;

    padding: 2.7rem 2.7rem;

    border-radius: 28px;

    background:
        linear-gradient(
            120deg,
            #5b55e7,
            #7c5ce7,
            #8464ff,
            #3478e5,
            #00aee8
        );

    background-size: 350% 350%;

    animation:
        heroGradient 12s ease infinite;

    box-shadow:
        0 20px 55px
        rgba(50, 55, 120, 0.23);

    margin-bottom: 2rem;
}


@keyframes heroGradient {

    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}


/* Decorative moving orbs */

.hero-orb-one {
    position: absolute;

    width: 190px;
    height: 190px;

    border-radius: 50%;

    background:
        rgba(255,255,255,0.10);

    right: -55px;
    top: -65px;

    animation:
        orbFloatOne 7s ease-in-out infinite;
}


.hero-orb-two {
    position: absolute;

    width: 105px;
    height: 105px;

    border-radius: 50%;

    background:
        rgba(255,255,255,0.09);

    right: 130px;
    bottom: -45px;

    animation:
        orbFloatTwo 6s ease-in-out infinite;
}


.hero-orb-three {
    position: absolute;

    width: 50px;
    height: 50px;

    border-radius: 50%;

    background:
        rgba(255,255,255,0.12);

    right: 260px;
    top: 35px;

    animation:
        orbFloatTwo 5s ease-in-out infinite reverse;
}


@keyframes orbFloatOne {

    0% {
        transform:
            translateY(0px)
            translateX(0px);
    }

    50% {
        transform:
            translateY(18px)
            translateX(-10px);
    }

    100% {
        transform:
            translateY(0px)
            translateX(0px);
    }
}


@keyframes orbFloatTwo {

    0% {
        transform:
            translateY(0px);
    }

    50% {
        transform:
            translateY(-15px);
    }

    100% {
        transform:
            translateY(0px);
    }
}


/* Hero icon */

.hero-icon {
    display: inline-block;

    font-size: 3rem;

    animation:
        heroIconFloat 3s ease-in-out infinite;

    margin-bottom: 0.3rem;
}


@keyframes heroIconFloat {

    0% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-7px);
    }

    100% {
        transform: translateY(0);
    }
}


.hero-title {
    color: #ffffff;

    font-size: 2.55rem;

    font-weight: 800;

    letter-spacing: -0.5px;

    margin-top: 0.3rem;
    margin-bottom: 0.6rem;
}


.hero-subtitle {
    color:
        rgba(255,255,255,0.90);

    max-width: 800px;

    font-size: 1.08rem;

    line-height: 1.75;

    margin-bottom: 0;
}


/* ============================================================
   STATUS BADGE
============================================================ */

.rag-status {
    display: inline-flex;

    align-items: center;

    gap: 9px;

    margin-top: 1.4rem;

    padding:
        8px 15px;

    border-radius: 30px;

    background:
        rgba(255,255,255,0.16);

    border:
        1px solid
        rgba(255,255,255,0.20);

    backdrop-filter: blur(8px);

    color: white;

    font-size: 0.87rem;

    font-weight: 650;
}


.status-dot {
    width: 9px;
    height: 9px;

    border-radius: 50%;

    background: #52f28d;

    animation:
        statusPulse 1.8s infinite;
}


@keyframes statusPulse {

    0% {
        box-shadow:
            0 0 0 0
            rgba(82,242,141,0.50);
    }

    70% {
        box-shadow:
            0 0 0 8px
            rgba(82,242,141,0);
    }

    100% {
        box-shadow:
            0 0 0 0
            rgba(82,242,141,0);
    }
}



/* ============================================================
   SECTION TITLES
============================================================ */

.section-label {
    margin-top: 1rem;

    margin-bottom: 1rem;

    color: #1f2937;

    font-size: 1.28rem;

    font-weight: 760;
}



/* ============================================================
   FEATURE CARDS
============================================================ */

.feature-card {
    min-height: 190px;

    padding: 1.45rem;

    border-radius: 20px;

    background:
        rgba(255,255,255,0.88);

    border:
        1px solid
        rgba(108,99,255,0.14);

    box-shadow:
        0px 10px 30px
        rgba(35,41,70,0.07);

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease,
        border-color 0.25s ease;

    position: relative;

    overflow: hidden;
}


.feature-card::before {
    content: "";

    position: absolute;

    top: 0;
    left: 0;

    width: 100%;
    height: 4px;

    background:
        linear-gradient(
            90deg,
            #6c63ff,
            #00c2ff,
            #ff6b6b
        );
}


.feature-card:hover {
    transform: translateY(-6px);

    border-color:
        rgba(108,99,255,0.42);

    box-shadow:
        0px 18px 42px
        rgba(74,70,160,0.14);
}


.feature-icon {
    font-size: 1.9rem;

    margin-bottom: 0.7rem;
}


.feature-title {
    color: #20263a;

    font-size: 1.03rem;

    font-weight: 750;

    margin-bottom: 0.45rem;
}


.feature-text {
    color: #667085;

    font-size: 0.93rem;

    line-height: 1.6;
}



/* ============================================================
   INFO STRIP
============================================================ */

.info-strip {
    display: flex;

    align-items: center;

    gap: 12px;

    padding:
        1rem 1.2rem;

    margin-top: 1rem;
    margin-bottom: 1.3rem;

    border-radius: 16px;

    background:
        linear-gradient(
            90deg,
            rgba(108,99,255,0.08),
            rgba(0,194,255,0.08)
        );

    border:
        1px solid
        rgba(108,99,255,0.12);

    color: #475467;

    font-size: 0.94rem;
}


.info-strip-icon {
    font-size: 1.4rem;
}



/* ============================================================
   CHAT MESSAGES
============================================================ */

div[data-testid="stChatMessage"] {
    border-radius: 18px;

    padding:
        0.75rem 0.9rem;

    margin-bottom: 0.9rem;

    background:
        rgba(255,255,255,0.91);

    border:
        1px solid
        rgba(108,99,255,0.10);

    box-shadow:
        0px 6px 20px
        rgba(35,41,70,0.05);
}



/* ============================================================
   BUTTONS
============================================================ */

.stButton > button {
    border-radius: 14px;

    min-height: 46px;

    border:
        1px solid
        rgba(108,99,255,0.22);

    background:
        linear-gradient(
            135deg,
            #ffffff,
            #f3f4ff
        );

    color: #3d3a8f;

    font-weight: 650;

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease,
        background 0.2s ease,
        color 0.2s ease;
}


.stButton > button:hover {
    border-color: #6c63ff;

    background:
        linear-gradient(
            135deg,
            #6c63ff,
            #755de8
        );

    color: #ffffff;

    transform: translateY(-2px);

    box-shadow:
        0px 9px 22px
        rgba(108,99,255,0.22);
}



/* ============================================================
   SOURCE EXPANDERS
============================================================ */

div[data-testid="stExpander"] {
    border:
        1px solid
        rgba(108,99,255,0.16);

    border-radius: 15px;

    background:
        rgba(249,250,255,0.95);
}



/* ============================================================
   CHAT INPUT
============================================================ */

div[data-testid="stChatInput"] {
    border-radius: 20px;
}



/* ============================================================
   SIDEBAR
============================================================ */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #f2f2ff,
            #f4f9ff
        );

    border-right:
        1px solid
        rgba(108,99,255,0.08);
}



/* ============================================================
   SIDEBAR BADGE
============================================================ */

.sidebar-badge {
    display: inline-block;

    padding:
        5px 10px;

    border-radius: 10px;

    background:
        rgba(108,99,255,0.10);

    color: #4f46a5;

    font-size: 0.78rem;

    font-weight: 700;

    margin-bottom: 0.8rem;
}



/* ============================================================
   SMALL ANIMATED SYMBOL
============================================================ */

.sparkle {
    display: inline-block;

    animation:
        sparklePulse 2.3s
        ease-in-out infinite;
}


@keyframes sparklePulse {

    0% {
        transform:
            scale(1)
            rotate(0deg);
    }

    50% {
        transform:
            scale(1.16)
            rotate(10deg);
    }

    100% {
        transform:
            scale(1)
            rotate(0deg);
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
<div class="sidebar-badge">
AI + Retrieval-Augmented Generation
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        "## 📚 RAG Study Assistant"
    )

    st.write(
        """
        A document-based AI assistant designed to make
        studying, revision, and information retrieval faster.
        """
    )

    st.divider()

    st.markdown(
        "### What can it help with?"
    )

    st.markdown(
        """
        **Understand concepts**  
        Ask for explanations of topics found in your course material.

        **Review lectures**  
        Revisit important information without manually opening every file.

        **Search documents**  
        Retrieve information from multiple course PDFs using semantic search.

        **Study with sources**  
        See which documents contributed to the generated answer.
        """
    )

    st.divider()

    st.markdown(
        "### RAG pipeline"
    )

    st.markdown(
        """
        `User Question`

        ↓

        `Question Embedding`

        ↓

        `Vector Search`

        ↓

        `Relevant Chunks`

        ↓

        `LLM Generation`

        ↓

        `Answer + Sources`
        """
    )

    st.divider()

    if st.button(
        "Clear conversation",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# HERO SECTION
# ============================================================

st.html(
    """
<div class="hero-container">
    <div class="hero-orb-one"></div>
    <div class="hero-orb-two"></div>
    <div class="hero-orb-three"></div>

    <div class="hero-icon">📚</div>

    <div class="hero-title">
        RAG Study Assistant
        <span class="sparkle">✦</span>
    </div>

    <div class="hero-subtitle">
        An AI-powered study assistant that searches your course
        documents, retrieves the most relevant information, and
        generates answers grounded in your learning material.
        <br><br>
        Ask questions, review difficult concepts, and locate
        information without manually searching through every
        lecture or PDF.
    </div>

    <div class="rag-status">
        <span class="status-dot"></span>
        Retrieval-Augmented Generation system online
    </div>
</div>
"""
)


# ============================================================
# FEATURE CARDS
# ============================================================

st.html(
    """
<div class="section-label">
    How this assistant helps you
</div>
"""
)

feature1, feature2, feature3 = st.columns(3)


with feature1:
    st.html(
        """
<div class="feature-card">
    <div class="feature-icon">🔎</div>

    <div class="feature-title">
        Semantic Retrieval
    </div>

    <div class="feature-text">
        Your question is converted into an embedding and compared
        with the document vector store to retrieve the most relevant
        chunks automatically.
    </div>
</div>
"""
    )


with feature2:
    st.html(
        """
<div class="feature-card">
    <div class="feature-icon">🧠</div>

    <div class="feature-title">
        Context-Aware Answers
    </div>

    <div class="feature-text">
        The retrieved course material is supplied to the language
        model so the generated explanation stays focused on the
        content of your documents.
    </div>
</div>
"""
    )


with feature3:
    st.html(
        """
<div class="feature-card">
    <div class="feature-icon">📄</div>

    <div class="feature-title">
        Source Transparency
    </div>

    <div class="feature-text">
        The assistant displays the source documents used during
        retrieval so you can trace the answer back to the original
        study material.
    </div>
</div>
"""
    )


st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# INFO STRIP
# ============================================================

st.html(
    """
<div class="info-strip">
    <div class="info-strip-icon">ℹ️</div>

    <div>
        Answers are generated from retrieved course content.
        If the required information is not present in the documents,
        the assistant should state that instead of relying on unrelated
        outside knowledge.
    </div>
</div>
"""
)


# ============================================================
# SUGGESTED QUESTIONS
# ============================================================

question = None


if len(st.session_state.messages) == 0:

    st.markdown(
        '<div class="section-label">'
        'Try a question'
        '</div>',
        unsafe_allow_html=True,
    )


    suggestion1, suggestion2, suggestion3 = (
        st.columns(3)
    )


    with suggestion1:

        if st.button(
            "Explain gradient descent",
            use_container_width=True,
        ):

            question = (
                "What is gradient descent?"
            )


    with suggestion2:

        if st.button(
            "Explain neural networks",
            use_container_width=True,
        ):

            question = (
                "What is a neural network?"
            )


    with suggestion3:

        if st.button(
            "Summarize the main concepts",
            use_container_width=True,
        ):

            question = (
                "Give me a short summary of the "
                "main concepts in the documents."
            )


    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        avatar = "👤"

    else:

        avatar = "🤖"


    with st.chat_message(
        message["role"],
        avatar=avatar,
    ):

        st.markdown(
            message["content"]
        )


        sources = message.get(
            "sources",
            [],
        )


        if sources:

            with st.expander(
                f"📚 Sources ({len(sources)})"
            ):

                for source in sources:

                    st.markdown(
                        f"• **{source}**"
                    )


# ============================================================
# USER INPUT
# ============================================================

typed_question = st.chat_input(
    "Ask a question about your course documents..."
)


if typed_question:

    question = typed_question


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    # --------------------------------------------------------
    # STORE USER MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )


    # --------------------------------------------------------
    # DISPLAY USER MESSAGE
    # --------------------------------------------------------

    with st.chat_message(
        "user",
        avatar="👤",
    ):

        st.markdown(
            question
        )


    # --------------------------------------------------------
    # GENERATE ASSISTANT ANSWER
    # --------------------------------------------------------

    with st.chat_message(
        "assistant",
        avatar="🤖",
    ):

        try:

            with st.spinner(
                "Searching the document store and generating an answer..."
            ):

                result = ask_backend(
                    question
                )


            answer = result["answer"]


            sources = result.get(
                "sources",
                [],
            )


            # ------------------------------------------------
            # DISPLAY ANSWER
            # ------------------------------------------------

            st.markdown(
                answer
            )


            # ------------------------------------------------
            # DISPLAY SOURCES
            # ------------------------------------------------

            if sources:

                st.caption(
                    "Answer grounded in "
                    f"{len(sources)} retrieved "
                    "source(s)"
                )


                with st.expander(
                    f"📚 View Sources ({len(sources)})"
                ):

                    for source in sources:

                        st.markdown(
                            f"• **{source}**"
                        )


            else:

                st.caption(
                    "No source documents were returned."
                )


            # ------------------------------------------------
            # STORE ASSISTANT RESPONSE
            # ------------------------------------------------

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                }
            )


        except Exception as error:

            st.error(
                "The assistant could not complete your request."
            )


            st.info(
                """
                Make sure the FastAPI backend and
                Ollama are both running.
                """
            )


            with st.expander(
                "Technical details"
            ):

                st.code(
                    str(error)
                )