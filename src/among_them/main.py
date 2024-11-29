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
        window.addEventListener('load', function() {
            function getTopWindow(currentWindow) {
                if (currentWindow.parent === currentWindow) {
                    return currentWindow;
                }
                return getTopWindow(currentWindow.parent);
            }

            const topWindow = getTopWindow(window);
            
            // Use MutationObserver to watch for changes in the DOM
            const observer = new MutationObserver(function(mutations) {
                // Get all divs in the top document
                const divs = topWindow.document.getElementsByTagName('div');
                // If there are divs
                if (divs.length > 0) {
                    // Get the last div
                    const lastDiv = divs[divs.length - 1];
                    // Check if it contains the profile container
                    if (lastDiv.className && lastDiv.className.includes('_profile')) {
                        lastDiv.remove();
                        // Disconnect the observer once we've found and removed the div
                        observer.disconnect();
                    }
                }
            });

            // Start observing the top document with the configured parameters
            observer.observe(topWindow.document, { childList: true, subtree: true });
        });
    </script>
    """
    st.components.v1.html(js, height=0)
    
    game_engine = GameEngine()

    game_engine.state.DEBUG = True
    game_engine.load_game()

    gui_handler.display_gui(game_engine)


if __name__ == "__main__":
    main()
