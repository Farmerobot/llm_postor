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
        function removeProfileContainers(topWindow) {
            try {
                const divs = topWindow.document.getElementsByTagName('div');
                console.log('Checking', divs.length, 'divs');
                
                Array.from(divs).forEach((div, index) => {
                    if (div.className && div.className.includes('_profileContainer')) {
                        console.log('Found profile div, removing...', div.className);
                        div.remove();
                    }
                });
            } catch (err) {
                console.error('Error removing containers:', err);
            }
        }

        function getTopWindow(currentWindow) {
            if (currentWindow.parent === currentWindow) {
                return currentWindow;
            }
            return getTopWindow(currentWindow.parent);
        }

        // Run immediately
        const topWindow = getTopWindow(window);
        removeProfileContainers(topWindow);

        // Also run frequently during page load
        const checkInterval = setInterval(() => {
            removeProfileContainers(topWindow);
        }, 100);

        // After 5 seconds, slow down the checks
        setTimeout(() => {
            clearInterval(checkInterval);
            // Set up observer for any future changes
            const observer = new MutationObserver(() => removeProfileContainers(topWindow));
            observer.observe(topWindow.document, { 
                childList: true, 
                subtree: true,
                attributes: true,
                attributeFilter: ['class']
            });
        }, 5000);
    </script>
    """
    st.components.v1.html(js, height=0)
    
    game_engine = GameEngine()

    game_engine.state.DEBUG = True
    game_engine.load_game()

    gui_handler.display_gui(game_engine)


if __name__ == "__main__":
    main()
