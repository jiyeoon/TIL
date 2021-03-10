import streamlit as st


class Toc:

    def __init__(self):
        self._items = []
        self._placeholder = None
    
    def title(self, text):
        self._markdown(text, "h1")

    def header(self, text):
        self._markdown(text, "h2", " " * 2)

    def subheader(self, text):
        self._markdown(text, "h3", " " * 4)

    def placeholder(self, sidebar=False):
        self._placeholder = st.sidebar.empty() if sidebar else st.empty()

    def generate(self):
        if self._placeholder:
            self._placeholder.markdown("\n".join(self._items), unsafe_allow_html=True)
    
    def _markdown(self, text, level, space=""):
        key = "".join(filter(str.isalnum, text)).lower()

        st.markdown(f"<{level} id='{key}'>{text}</{level}>", unsafe_allow_html=True)
        self._items.append(f"{space}* <a href='#{key}'>{text}</a>")


toc = Toc()

st.title("Table of contents")
toc.placeholder(sidebar=True)

toc.title("Title")

for a in range(10):
    st.write("Blabla...")

toc.header("Header 1")

for a in range(10):
    st.write("Blabla...")

toc.header("Header 2")

for a in range(10):
    st.write("Blabla...")

toc.subheader("Subheader 1")

for a in range(10):
    st.write("Blabla...")

toc.subheader("Subheader 2")

for a in range(10):
    st.write("Blabla...")

toc.generate()