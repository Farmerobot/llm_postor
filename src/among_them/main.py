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
            console.log('Script loaded and running');
            
            function getTopWindow(currentWindow) {
                console.log('Current window location:', currentWindow.location.href);
                if (currentWindow.parent === currentWindow) {
                    console.log('Found top window');
                    return currentWindow;
                }
                console.log('Moving up to parent window');
                return getTopWindow(currentWindow.parent);
            }

            try {
                console.log('Getting top window...');
                const topWindow = getTopWindow(window);
                console.log('Top window location:', topWindow.location.href);
                
                const observer = new MutationObserver(function(mutations) {
                    console.log('DOM mutation detected');
                    try {
                        const divs = topWindow.document.getElementsByTagName('div');
                        console.log('Found', divs.length, 'divs');
                        
                        // Convert to array to avoid live collection issues when removing elements
                        Array.from(divs).forEach((div, index) => {
                            console.log(`Checking div ${index}:`, div.className);
                            if (div.className && 
                                (div.className.includes('_profileContainer') || 
                                 div.className.includes('_profile'))) {
                                console.log('Found profile div, removing...', div.className);
                                div.remove();
                                console.log('Profile div removed');
                            }
                        });
                    } catch (err) {
                        console.error('Error in observer callback:', err);
                    }
                });

                console.log('Setting up observer...');
                observer.observe(topWindow.document, { 
                    childList: true, 
                    subtree: true,
                    attributes: true,
                    attributeFilter: ['class']
                });
                console.log('Observer setup complete');
            } catch (err) {
                console.error('Error in main script:', err);
            }
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
