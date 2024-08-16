import os
import requests
import zipfile
import shutil
import gitClass
from colorama import Fore, Back, Style
class WpUpdate:
    #Functions Update plugins

    def get_plugin_versions(self,wp_path):
        plugins_path = os.path.join(wp_path, 'wp-content', 'plugins')
        plugins = {}

        if os.path.exists(plugins_path):
            for plugin in os.listdir(plugins_path):
                plugin_path = os.path.join(plugins_path, plugin)
                if os.path.isdir(plugin_path):
                    plugin_file = os.path.join(plugin_path, 'readme.txt')
                    if os.path.exists(plugin_file):
                        try:
                            with open(plugin_file, 'r', encoding='utf-8') as f:
                                for line in f:
                                    if 'Stable tag:' in line:
                                        version = line.split(':')[1].strip()
                                        plugins[plugin] = version
                                        break
                        except UnicodeDecodeError:
                            with open(plugin_file, 'rb') as f:
                                raw_data = f.read()
                                result = chardet.detect(raw_data)
                                encoding = result['encoding']
                                with open(plugin_file, 'r', encoding=encoding) as f:
                                    for line in f:
                                        if 'Stable tag:' in line:
                                            version = line.split(':')[1].strip()
                                            plugins[plugin] = version
                                            break
        return plugins

    def get_latest_plugin_version(self,plugin_slug):
        try:
            response = requests.get(f'https://api.wordpress.org/plugins/info/1.2/?action=plugin_information&request[slug]={plugin_slug}')
            if response.status_code == 200:
                plugin_data = response.json()
                return plugin_data.get('version', 'Unknown')
        except Exception as e:
            print(Fore.RED + f"Error occurred while fetching version for {plugin_slug}: {e}" + Style.RESET_ALL)
        return 'Unknown'

    def download_latest_plugin(self,plugin_slug):
        try:
            response = requests.get(f'https://downloads.wordpress.org/plugin/{plugin_slug}.latest-stable.zip', stream=True)
            if response.status_code == 200:
                zip_path = f'{plugin_slug}.zip'
                with open(zip_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                return zip_path
        except Exception as e:
            print(Fore.RED +  f"Error occurred while downloading plugin {plugin_slug}: {e}" + Style.RESET_ALL)
        return None

    def update_plugin(self,wp_path, plugin_slug):
        zip_path = self.download_latest_plugin(plugin_slug)
        if zip_path:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(wp_path)
            os.remove(zip_path)
            print(Fore.GREEN + f"Plugin {plugin_slug} updated successfully." + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Failed to download the latest version of {plugin_slug}." + Style.RESET_ALL)

    def check_and_update_plugins(self,wp_path):
        plugins = self.get_plugin_versions(wp_path)
        gitObj = gitClass.GitApp(wp_path)
        if not plugins:
            print(Fore.YELLOW +  "No plugins found or unable to read plugin versions." + Style.RESET_ALL)
            return

        for plugin, installed_version in plugins.items():
            latest_version = self.get_latest_plugin_version(plugin)
            if latest_version == 'Unknown':
                print(Fore.RED + f"Could not fetch the latest version for plugin: {plugin}" + Style.RESET_ALL)
            elif installed_version != latest_version:
                print(Fore.BLUE + f"Plugin '{plugin}' is outdated. Installed version: {installed_version}, Latest version: {latest_version}. Updating..." + Style.RESET_ALL)
                self.update_plugin(os.path.join(wp_path, 'wp-content', 'plugins'), plugin)
                gitObj.add_all()
                gitObj.commit_changes(Fore.GREEN +  f"Updating Plugin {plugin} from version {installed_version} to {latest_version}." + Style.RESET_ALL)
                #git commit 
            else:
                print(Fore.YELLOW + f"Plugin '{plugin}' is up-to-date (Version: {installed_version})." + Style.RESET_ALL)


    #Functions Update Core
    def get_wp_version(self,wp_path):
        version_file_path = os.path.join(wp_path, 'wp-includes', 'version.php')
        if os.path.exists(version_file_path):
            with open(version_file_path, 'r') as version_file:
                for line in version_file:
                    if line.startswith("$wp_version"):
                        version = line.split('=')[1].strip().strip(';').strip("'")
                        return version
        return None

    def get_latest_wp_version(self):
        try:
            response = requests.get('https://api.wordpress.org/core/version-check/1.7/')
            if response.status_code == 200:
                latest_version = response.json()['offers'][0]['version']
                return latest_version
        except Exception as e:
            print(Fore.RED + "Error occurred while fetching the latest WordPress version:" + Style.RESET_ALL, e)
        return None

    def download_latest_wp(self,latest_version):
        download_url = f'https://wordpress.org/wordpress-{latest_version}.zip'
        try:
            response = requests.get(download_url)
            if response.status_code == 200:
                zip_path = f'wordpress-{latest_version}.zip'
                with open(zip_path, 'wb') as file:
                    file.write(response.content)
                return zip_path
        except Exception as e:
            print(Fore.RED + "Error occurred while downloading the latest WordPress version:" + Style.RESET_ALL, e)
        return None

    def extract_zip(self,zip_path, extract_to):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

    def update_wp(self,wp_path, latest_version):
        zip_path = self.download_latest_wp(latest_version)
        if zip_path:
            extract_to = f'{wp_path}tmp'
            self.extract_zip(zip_path, extract_to)
            
            # Move files from the extracted directory to the WordPress installation
            extracted_wp_path = os.path.join(extract_to, 'wordpress')
            for item in os.listdir(extracted_wp_path):
                source = os.path.join(extracted_wp_path, item)
                destination = os.path.join(wp_path, item)
                if os.path.exists(destination):
                    if os.path.isdir(destination):
                        if item != 'wp-content':
                            shutil.rmtree(destination)
                            shutil.copytree(source, destination)
                    else:
                        os.remove(destination)
                        shutil.copy2(source, destination)
                else:
                    shutil.copytree(source, destination) if os.path.isdir(source) else shutil.copy2(source, destination)
            
            # Clean up
            os.remove(zip_path)
            shutil.rmtree(extract_to)
            print(Fore.GREEN + "WordPress updated successfully." + Style.RESET_ALL)
        else:
            print(Fore.RED + "Failed to download the latest WordPress version." + Style.RESET_ALL)
