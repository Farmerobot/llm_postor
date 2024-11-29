import streamlit as st

from among_them.game.game_engine import GameEngine
from among_them.game.gui_handler import GUIHandler

# To run this script, you need to
# `poetry install`
# and then run the following command:
# `poetry run main`


def main():
    gui_handler = GUIHandler()
    st.set_page_config(page_title="Among Them", layout="wide")
    
    # Inject JavaScript to remove the footer
    js = """
    <script>
        // Inject CSS immediately to hide the element before we can remove it
        const style = document.createElement('style');
        style.textContent = `
            div[class*='_profileContainer'] { 
                display: none !important;
                opacity: 0 !important;
                visibility: hidden !important;
            }
        `;
        document.head.appendChild(style);

        function removeProfileContainers(topWindow) {
            try {
                const divs = topWindow.document.getElementsByTagName('div');
                Array.from(divs).forEach(div => {
                    if (div.className?.includes('_profileContainer')) {
                        div.remove();
                    }
                });
            } catch (err) {}
        }

        function getTopWindow(currentWindow) {
            if (currentWindow.parent === currentWindow) return currentWindow;
            return getTopWindow(currentWindow.parent);
        }

        // Run as early as possible
        try {
            const topWindow = getTopWindow(window);
            
            // Inject the CSS into top window as well
            const topStyle = topWindow.document.createElement('style');
            topStyle.textContent = style.textContent;
            topWindow.document.head.appendChild(topStyle);

            // Run immediately
        } catch (err) {}
    </script>
    """
    st.components.v1.html(js, height=0)
    
    game_engine = GameEngine()

    game_engine.state.DEBUG = True
    game_engine.load_game()

    gui_handler.display_gui(game_engine)


if __name__ == "__main__":
    main()
