from datetime import datetime
import os
import wpUpdate
import gitClass
import animation
from colorama import Fore, Back, Style
from animation import loading_animation,welcome_animation,end_animation



def main():
    while True:
        path = input("Please enter the correct path: ")
        loading_animation(3)
        if os.path.exists(path):
            wordpress_path = path  
            gitObj = gitClass.GitApp(wordpress_path)
            WpUpdateObj = wpUpdate.WpUpdate()

            current_version = WpUpdateObj.get_wp_version(wordpress_path)
            latest_version = WpUpdateObj.get_latest_wp_version()

            current_date = datetime.now()
            month = current_date.strftime('%m')
            year = current_date.strftime('%y')
            BranchName = f'feature/update-{month}-{year}'

            if current_version and latest_version:
                if current_version != latest_version:
                    print(Fore.GREEN + f"Updating WordPress from version {current_version} to {latest_version}."+ Style.RESET_ALL)
                    WpUpdateObj.update_wp(wordpress_path, latest_version)
                    if gitObj.branch_exists(BranchName) == True : 
                        if gitObj.is_current_branch(BranchName) == False:
                            gitObj.checkout_branch(BranchName)
                    else:
                        gitObj.create_and_checkout_branch(BranchName)
                    gitObj.add_all()
                    gitObj.commit_changes(Fore.GREEN + f"Updating WordPress from version {current_version} to {latest_version}."+ Style.RESET_ALL)
                else:
                    print(Fore.YELLOW + "You have the latest version of WordPress installed."+ Style.RESET_ALL)
            else:
                print(Fore.RED + "Unable to compare versions. Please check your WordPress installation and network connection."+ Style.RESET_ALL)

            #Update plugins : 

            if gitObj.branch_exists(BranchName) == True : 
                if gitObj.is_current_branch(BranchName) == False:
                    gitObj.checkout_branch(BranchName)
            else:
                gitObj.create_and_checkout_branch(BranchName)

            WpUpdateObj.check_and_update_plugins(wordpress_path)
            return
        else:
            print(Fore.RED + "Invalid path. Please try again."+ Style.RESET_ALL)

if __name__ == "__main__":
    welcome_animation()
    main()
    end_animation()
    input("Press Enter to exit...")
    