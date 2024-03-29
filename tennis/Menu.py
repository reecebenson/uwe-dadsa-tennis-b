"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
import traceback
from tennis.Colours import Colours
from functools import partial
from os import system as call
from collections import OrderedDict

class Menu():
    # Define our Game
    game = None

    def __init__(self, _game):
        self.game = _game

    def load(self, reloading = False):
        # Temporary Menu Debug
        menu_debug = True

        # Create our Menu
        Builder().init(self.game, False, reloading)

        ## MAIN ------------------------------------------------------------------------------------------------------------------------------
        Builder().add_menu("main", "Load Game", "loadgame")
        Builder().add_info("loadgame", "List the seasons within this Tennis game.")
        Builder().add_menu("main", "Developer Information", "info")
        Builder().add_info("info", "Show information about the developer.")
        if(menu_debug): Builder().add_menu("main", "Debugging", "debug")
        Builder().add_func("main", "info", partial(print, "Created by Reece Benson, 16021424."))

        ## SEASONS ---------------------------------------------------------------------------------------------------------------------------
        for season in self.game.seasons:
            # Variables
            season_obj = self.game.seasons[season]
            season_id = season[-1:]

            # Add Season
            Builder().add_menu("loadgame", "Season {}{}".format(season_id, Colours.OKGREEN + " (Available)" + Colours.ENDC if season_obj.is_available() else ""), "view_{}".format(season))

            # Check that this season is available
            if(not season_obj.is_available()):
                continue

            ## TOURNAMENTS -------------------------------------------------------------------------------------------------------------------
            for tournament in self.game.seasons[season].get_tournaments():
                Builder().add_menu("view_{}".format(season), "{}{}".format(tournament.get_name(), Colours.OKGREEN + " (Complete)" + Colours.ENDC if tournament.is_complete() else Colours.FAIL + " (Incomplete)" + Colours.ENDC), "s{}_t{}".format(season_obj.get_id(), tournament.get_name()))

                ## ROUNDS --------------------------------------------------------------------------------------------------------------------
                for t_round in tournament.get_rounds():
                    Builder().add_menu("s{}_t{}".format(season_obj.get_id(), tournament.get_name()), "Round {}".format(t_round.get_id()), "s_{}_t{}_r{}".format(season_obj.get_id(), tournament.get_name(), t_round.get_id()))

                    ## GENDERS ---------------------------------------------------------------------------------------------------------------
                    for gdr in t_round.get_genders():
                        Builder().add_menu("s_{}_t{}_r{}".format(season_obj.get_id(), tournament.get_name(), t_round.get_id()), "{}{}".format(gdr[0].title(), Colours.OKGREEN + " (Complete)" + Colours.ENDC if gdr[1].is_complete() else (Colours.FAIL + " (Incomplete)" + Colours.ENDC if gdr[1].is_available() else "")), "s_{}_t{}_r{}_g{}".format(season_obj.get_id(), tournament.get_name(), t_round.get_id(), gdr[0]))

                        ## CHECK GENDER IS AVAILABLE -----------------------------------------------------------------------------------------
                        if(gdr[1].is_available()):
                            Builder().add_func("s_{}_t{}_r{}".format(season_obj.get_id(), tournament.get_name(), t_round.get_id()), "s_{}_t{}_r{}_g{}".format(season_obj.get_id(), tournament.get_name(), t_round.get_id(), gdr[0]), partial(gdr[1].run))

            ## OVERALL RANKINGS --------------------------------------------------------------------------------------------------------------
            Builder().add_menu("view_{}".format(season), "View Overall Data", "overall_{}".format(season))
            Builder().add_menu("overall_{}".format(season), "View Overall Ranking Points", "overall_rp_{}".format(season))
            Builder().add_menu("overall_{}".format(season), "View Overall Prize Money", "overall_pm_{}".format(season))

            ## OVERALL RANKINGS GENDER -------------------------------------------------------------------------------------------------------
            for or_gender in season_obj.get_genders():
                Builder().add_menu("overall_rp_{}".format(season), or_gender.title(), "overall_rp_{}_{}".format(season, or_gender))
                Builder().add_menu("overall_pm_{}".format(season), or_gender.title(), "overall_pm_{}_{}".format(season, or_gender))
                Builder().add_func("overall_rp_{}".format(season), "overall_rp_{}_{}".format(season, or_gender), partial(season_obj.view_overall_ranking_points, or_gender))
                Builder().add_func("overall_pm_{}".format(season), "overall_pm_{}_{}".format(season, or_gender), partial(season_obj.view_overall_prize_money, or_gender))

            ## DEBUG -------------------------------------------------------------------------------------------------------------------------
            if(self.game.debug):
                Builder().add_menu("view_{}".format(season), "Complete All Tournaments", "complete_{}".format(season))
                Builder().add_func("view_{}".format(season), "complete_{}".format(season), partial(season_obj.force_complete))

            ## STATISTCAL ANALYSIS -----------------------------------------------------------------------------------------------------------
            Builder().add_menu("view_{}".format(season), "Statistical Analysis", "stats_{}".format(season))
            Builder().add_func("view_{}".format(season), "stats_{}".format(season), partial(season_obj.statistical_analysis))

        # Show Menu
        Builder().show_current_menu()


"""Start of Menu Builder Class"""        
class Builder():
    game = None
    _menu = None
    _tree = None
    _current = None
    _title = None
    _force_close = None
    _force_reload = None

    @staticmethod
    def init(game, title = False, reloading = False):
        # Set our variables
        Builder.game = game
        Builder._menu = { }

        # Flags will be reset when the menu is closed and reinitialised, or when the menu is closed and then reloaded (init called again)
        Builder._force_close = False
        Builder._force_reload = False

        # If we're reloading, don't reset our current pos or data related to current open menu
        if(not reloading):
            # Set our other variables
            Builder._tree = [ "main" ]
            Builder._current = "main"
            Builder._title = "Please select an option:" if not title else title

    @staticmethod
    def close_menu():
        # Set our flag
        Builder._force_close = True

    @staticmethod
    def reload_menu():
        # We will pop() [go back] to avoid hitting any errors (maybe menu is replaced with a function, etc)
        #Builder.go_back(True)

        # Set our flag
        Builder._force_reload = True

    @staticmethod
    def add_menu(menu, name, ref):
        # Check if this submenu exists
        if(not menu in Builder._menu):
            Builder._menu[menu] = { }

        # Update our Menu
        Builder._menu[menu].update({ ref: name })

    @staticmethod
    def add_info(ref, info):
        # Add additional information to a menu item
        Builder._menu[ref+"_info"] = info

    @staticmethod
    def add_func(name, ref, func):
        # Add a selectable function to the referred menu item
        Builder._menu[ref] = func

    @staticmethod
    def get_item(ref):
        # Get an existing item, otherwise return None
        if(not ref in Builder._menu):
            return None
        else:
            return Builder._menu[ref]
        return None

    @staticmethod
    def call_func(ref):
        # Call the function reference of a menu item
        if(Builder.is_func(ref)):
            return Builder.get_item(ref)()
        else:
            return None

    @staticmethod
    def is_func(ref):
        # Check if the function reference is callable / is a function
        return callable(Builder.get_item(ref))

    @staticmethod
    def item_exists(ref):
        # Check if a menu item or reference exists
        return (ref in Builder._menu)

    @staticmethod
    def is_menu(ref):
        # Set flag
        is_a_menu = True
        
        # Check if the "menu" exists
        if(not ref in Builder._menu):
            is_a_menu = False

        # Check if the menu is a dictionary
        if(type(Builder.get_item(ref)) != dict):
            is_a_menu = False

        return is_a_menu

    @staticmethod
    def notAvailable(text):
        # Append a string as a suffix
        return text + " {0}(Not Available){1}".format(Colours.FAIL, Colours.ENDC)

    @staticmethod
    def find_menu(index):
        # Get our current menu to check the items for
        cur_menu_items = Builder.get_item(Builder.current_menu())

        # Check that our menu exists
        if(cur_menu_items == None):
            print("There was an error with grabbing the selected menu!")
            Builder.set_current_menu("main")
            return False
        else:
            # Iterate through our items to find our index
            for i, (k, v) in enumerate(cur_menu_items.items(), 1):
                if(index == i):
                    return { "menu": Builder.is_menu(k), "ref": k, "name": v }

            # Return Data
            return False

        # Fall back returning statement
        return False

    @staticmethod
    def show():
        # Print a tree of the current built menu
        print(Builder._menu)

    @staticmethod
    def current_menu():
        # Return the current menu (top of the stack)
        return Builder._current

    @staticmethod
    def set_current_menu(new_menu):
        # Set the current menu
        Builder._current = new_menu
        return Builder.current_menu()

    @staticmethod
    def add_menu_tree(ref):
        # Add to our current menu tree
        Builder._tree.append(ref)

    @staticmethod
    def get_menu_tree():
        # Get our current menu tree as a string, split by forward slash (/)
        return "/".join([ m for m in Builder._tree ])

    @staticmethod
    def go_back(reloading = False):
        # Set our flag to true
        Builder.just_called_back = True

        # Pop off the last item of the list
        Builder._tree.pop()

        # Set our current menu to the last element of the list
        Builder._current = Builder._tree[-1]

        # Display our menu
        if(not reloading):
            return Builder.show_current_menu()

        return None

    @staticmethod
    def monitor_input():
        # Check if we're force closing the menu or if we're reloading the menu
        if(Builder._force_close):
            return

        try:
            # Validate our input
            resp = input("\n>>> ")

            # Validate response
            if(resp.lower() == "exit" or resp.lower() == "quit" or resp.lower() == "x"):
                # Terminate the program after user confirmation
                raise KeyboardInterrupt
            elif(resp == ""):
                # Invalid Input from User
                return Builder.show_current_menu(True, True, "You have entered an invalid option")

            # Check that the menu option exists
            try:
                # See if we're trying to go back a page
                if(resp.lower() == "b" and Builder._current is not "main"):
                    return Builder.go_back()

                # Convert our request to an integer
                req = int(resp)

                # Find the requested menu
                req_menu = Builder.find_menu(req)
                if(type(req_menu) == dict):
                    if(req_menu['menu']):
                        # Display our menu
                        Builder.set_current_menu(req_menu['ref'])
                        Builder.add_menu_tree(req_menu['ref'])
                        Builder.show_current_menu()
                    else:
                        # Double check we're executing a function
                        if(Builder.is_func(req_menu['ref'])):
                            # Clear Terminal
                            call("cls")

                            # Print Function Header
                            if(Builder.game.debug):
                                print(" _______ ______ _   _ _   _ _____  _____ ")
                                print("|__   __|  ____| \\ | | \\ | |_   _|/ ____|")
                                print("   | |  | |__  |  \\| |  \\| | | | | (___  ")
                                print("   | |  |  __| | . ` | . ` | | |  \\___ \\ ")
                                print("   | |  | |____| |\\  | |\\  |_| |_ ____) |")
                                print("   |_|  |______|_| \\_|_| \\_|_____|_____/ ")
                            print("——————————————————————————————————————————————————————————————")

                            # Execute
                            retStr = Builder.call_func(req_menu['ref'])

                            # Hold user (to display output from function)
                            if(retStr != "SKIP"):
                                input("\n>>> Press <Return> to continue...")

                            if(not Builder._force_reload):
                                return Builder.show_current_menu()
                            else:
                                Builder.game.menu = Menu(Builder.game)
                                return Builder.game.menu.load(True)
                        else:
                            if(not Builder.item_exists(req_menu['ref'])):
                                return Builder.show_current_menu(True, True, "That option is unavailable")
                            else:
                                if(req_menu['ref'] == "return"):
                                    # User wants to go back to the default menu
                                    input("\nYou are now going to the main menu!\nWarning: If data has not been added, rounds will not exist!")
                else:
                    # Check if we pressed the Back button
                    current_menu = Builder.get_item(Builder._current)
                    if(req == (len(current_menu) + 1) and Builder._current is not "main"):
                        return Builder.go_back()
                    elif(req == (len(current_menu) + 1) and Builder._current is "main"):
                        return Builder.game.exit()
                    else:
                        return Builder.show_current_menu(True, True, "You have entered an invalid option")
            # Exceptions (handled from outer-scope try/except)
            except KeyboardInterrupt:   raise KeyboardInterrupt
            except ValueError:          raise ValueError
            except Exception:           raise Exception

        # Exceptions
        except KeyboardInterrupt:
            # User has terminated the program (Ctrl+C)
            return Builder.game.exit()
        except ValueError:
            # User has entered an invalid value
            return Builder.show_current_menu(True, True, "You have entered an invalid option")
        except Exception:
            # Handle other exceptions, and if debugging - show the error and halt the application
            if(Builder.game.debug):
                print("{1}\nERROR:\nError Handled:\n{0}\n{2}".format(traceback.print_exc(), Colours.FAIL, Colours.ENDC))
                input("...continue")
            # Application has handled error for User
            return Builder.show_current_menu(True, True)

    @staticmethod
    def show_current_menu(shouldClear = True, error = False, errorMsg = None):
        cur_menu_items = Builder.get_item(Builder.current_menu())

        # Should we clear our terminal window?
        if(shouldClear):
            call("cls")

        # Have we got an error?
        if(error):
            if(errorMsg == None):
                print("\n{0}{1}Error:{2}\n{0}There was an error performing your request.{2}\n".format(Colours.FAIL, Colours.BOLD, Colours.ENDC))
            else:
                print("\n{2}Error:{3}\n{1}{0}.{3}\n".format(errorMsg, Colours.FAIL, Colours.BOLD, Colours.ENDC))

        # Check that our Menu exists
        if(cur_menu_items == None):
            print("{}There was an error with grabbing the selected menu!{}".format(Colours.FAIL, Colours.ENDC))
            print("Current menu: {}".format(Builder.current_menu()))
            Builder.set_current_menu("main")
        else:
            # Print menu header
            print("{2}{0}{3} ({4}{1}{3})".format(Builder._title, Builder.get_menu_tree(), Colours.BOLD, Colours.ENDC, Colours.GRAY))
            
            # Print out our menu
            for i, (k, v) in enumerate(cur_menu_items.items(), 1):
                if(Builder.item_exists(k)):
                    print("{3}{0}{4}. {1}{2}".format(i, v, (' -> ' if Builder.is_menu(k) else ''), Colours.BOLD + Colours.OKGREEN, Colours.ENDC))
                else:
                    print(Builder.notAvailable("{3}{0}{4}. {1}{2}".format(i, v, (' -> ' if Builder.is_menu(k) else ''), Colours.BOLD + Colours.OKGREEN, Colours.ENDC)))

                # Does this key (ref) have info?
                if(Builder.item_exists(k+"_info")):
                    print("   - {0}{1}".format(Builder.get_item(k+"_info"), "" if (i == len(cur_menu_items.items()) and Builder.current_menu() is "main") else "\n"))

            # Print our back button
            print("{0}".format("{0}b{1}. Back".format(Colours.FAIL, Colours.ENDC) if Builder.current_menu() is not "main" else "{0}x{1}. Exit and Save".format(Colours.FAIL, Colours.ENDC)))

            # Get input from user
            Builder.monitor_input()