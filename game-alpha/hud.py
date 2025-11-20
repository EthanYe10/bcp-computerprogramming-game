class HUD: 
    """class HUD
    author: Ethan Ye
    this class handles the HUD as well as game stats and progress
    it would more fittingly called game manager but that name's too long
    the vision for this would be to have a singleton and read from a save file instead of refreshing every time the game loop ends
    """
    def __init__(self, game):
        self.game = game
        self.font = pg.font.Font(None, 25)

        """elements of adventure to HUD:
        - no health (dies in 1 hit)
        - score (each enemy killed adds to score)
        - which section of map player is in (maze, castle, etc.)
        - timer (how fast to beat game)
        - progress bar (what you have accomplished)
        - high score
        strong typing because i'm a c++/java nerd and I value autocomplete"""
        self.score: int = 0
        self.timer: int = 0
        self.high_score: int = 0
        self.location: str = ""
        self.progress: dict = {
            'items' : { # tracks what items you have collected
                'chalice': False,
                'sword': False,
                'bridge' : False, 
                'magnet' : False, 
                'yellow_key' : False,
                'black_key' : False,
                'white_key' : False
            }, 
            'enemies' : { # tracks what enemies you have defeated
                'green_dragon' : False,
                'red_dragon' : False,
                'yellow_dragon' : False
            }, 
            'locations' : { # tracks what locations you have visited
                # maze is a number 0-100 representing percentage completed
                'black_castle' : False, 
                'white_castle' : False,
                'gold_castle' : False, 
                'maze' : 0
            }
        }
    