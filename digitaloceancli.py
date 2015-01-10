"""
DigitalOcean Console Application
1.0.0
Author: Yusuf Tuğrul Kocaman
"""
import sys
import cmd
import getpass
import requests
from tabulate import tabulate
from colorama import init
from termcolor import cprint, colored
import digitalocean
from digitalocean import DataReadError, DropletError

OUTPUT_TYPES = {
    'success' : 'green',
    'error'   : 'red',
    'info'    : 'yellow',
    'default' : 'white'
}

def print_log(msg, type='info'):
    print(colored(msg, OUTPUT_TYPES[type]))
    
class DigitalOcean(cmd.Cmd):
    """
    DigitalOcean Console Client Class
    """
    use_rawinput = False
    account = None
    uniqueKey = None
    prompt = colored(">>", "magenta")
    intro = "Welcome to DigitalOcean Shell. Type help or ? to list commands. \n"
    manager = None
    """
    Selected droplet.
    """
    droplet = None 
    
    def help_login(self):
        print_log("Login with your unique DigitalOcean API key. If you don't have, please see: https://cloud.digitalocean.com/settings/applications", "info")
    
    def _try_login(self, password):
        try:
            tmpManager = digitalocean.Manager(token=password)
            self.account = tmpManager.get_account()
            self.uniqueKey = password
            print_log("Successfully logged in!", "success")
            self.manager = tmpManager
        except DataReadError as err:
            print_log(err, "error")
        except requests.ConnectionError as err:
            print_log("Connection error!", "error") 

    def help_account_info(self):
        print_log("Shows your account information based on API.","info")
        
    def do_account_info(self, line):
        if self.account:
            headers = ["E-Mail","Email Verified", "Droplet Limit", "UUID"]
            table = [
                [self.account.email, self.account.email_verified,
                self.account.droplet_limit, self.account.uuid]
            ]
            print_log(tabulate(table, headers, tablefmt="grid", numalign="center", stralign="center"), "info")
        else:
            print_log("Login first!", "info")
            
    def do_login(self, line):
        if self.uniqueKey:
            answer = input("You have already logged in. Would you like to login again? [Y\n]")
            if answer.lower() == "y":
                password = getpass.getpass("API Key:")
                if len(password) > 5:
                    self._try_login(password)
                self.uniqueKey = None
            else:
                print_log("Login cancelled!", "info")
        else:
            password = getpass.getpass("API Key:")
            if len(password) > 5:
                self._try_login(password)
            else:
                print_log("Please enter a token!", "error")

    def do_about(self, line):
        print("#---------------------------------------------#")
        print("#              {0}           #".format(colored("Yusuf Tuğrul Kocaman","cyan")))
        print("#          {0}   : {1}         #".format(colored("github","green"), colored("kulturlupenguen","magenta")))
        print("#---------------------------------------------#")
    
    def help_clear(self):
        print_log("Clear the screen.", "info")

    def do_clear(self, line):
        sys.stderr.write("\x1b[2J\x1b[H")
            
    def help_exit(self):
         print_log("Exits the interface.","error")

    def do_exit(self, line):
         print_log("Thank you for using DigitalOcean CLI by kulturlupenguen", "success")
         import time
         time.sleep(0.1)
         sys.exit(0)
         
    def do_EOF(self, line):
        return True
    
    def help_ls(self):
        print_log("Lists all of your droplets.", "info")

    def do_ls(self, line):
        if self.uniqueKey:
            droplets = self.manager.get_all_droplets()
            headers = ['ID', 'Name', 'Status',' Memory (MB)', 'CPU(s)', 'Disk (GB)', 'IP']
            table = []
            for droplet in droplets:
                table.append(
                    [
                        droplet.id, droplet.name, droplet.status, droplet.memory, droplet.vcpus,
                        droplet.disk, droplet.ip_address
                    ]
                )
            print_log(tabulate(table, headers, tablefmt="grid", numalign="center", stralign="center"), "success")
        else:
            print_log("Login first!", "error")

    def help_select(self):
        print_log("Selects droplet by ID.If you don't know your ID please type \"ls\".", "info")

    def do_select(self, droplet_id):
        if self.manager:
            try:
                if len(droplet_id) > 1:
                    droplet = self.manager.get_droplet(droplet_id)
                    print_log("Droplet {0} ({1}) has been successfully selected!".format(droplet.name, droplet.id), "success")
                    self.droplet = droplet
                else:
                    self.droplet = None
                    print_log("Please enter a droplet ID!", "error")
            except DataReadError as err:
                print_log(err, "error")
        else:
            print_log("Login first!", "error")

    def help_status(self):
        print_log("Shows the current status of the droplet you have selected.", "info")

    def do_status(self, line):
        if self.droplet:
            status = "Droplet Name: {0}\n".format(colored(self.droplet.name, "magenta"))
            status += "Droplet ID: {0}\n".format(colored(self.droplet.id, "magenta"))
            status += "Memory (MB): {0}\n".format(colored(self.droplet.memory, "magenta"))
            status += "CPU Count: {0}\n".format(colored(self.droplet.vcpus, "magenta"))
            status += "Disk (GB): {0}\n".format(colored(self.droplet.disk, "magenta"))
            status += "Status: {0}\n".format(colored(self.droplet.status, "magenta"))
            status += "Region: {0}\n".format(colored(self.droplet.region['name'], "magenta"))
            status += "Created: {0}\n".format(colored(self.droplet.created_at, "magenta"))
            status += "IP Address: {0}\n".format(colored(self.droplet.ip_address, "magenta"))
            status += "OS Information: {0} {1} ({2})\n".format(colored(self.droplet.image['distribution'], "red"), colored(self.droplet.image['name'], "blue"), colored(self.droplet.kernel['name'], "yellow"))
            print(status)
        else:
            print_log("Select a droplet first!", "error")
    
    def help_restart(self):
        print_log("Power cycle selected droplet.", "info")
        
    def do_restart(self, line):
        if self.droplet:
            result = self.droplet.power_cycle()
            try:
                if result['action']['status'] in ['in-progress','completed']:
                    print_log("Your command has been executed on your droplet! Current status is {0}".format(result['action']['status']), "success")
            except DropletError as err:
                print_log(err, "error")
        else:
            print_log("Select a droplet first!", "error")

    def help_shutdown(self):
        print_log("Shutdown selected droplet.", "info")

    def do_shutdown(self, line):
        if self.droplet:
            if self.droplet.status == 'off':
                print_log("Droplet is off already.", "error")
            else:
                result = self.droplet.shutdown()
                try:
                    if result['action']['status'] in ['in-progress','completed']:
                        print_log("Your droplet is shutdowned!", "success")
                except DropletError as err:
                    print_log(err, "error")
        else:
            print_log("Select a droplet first!", "error")

    def help_bootup(self):
        print_log("Power on selected droplet.", "info")

    def do_bootup(self, line):
        if self.droplet:
            if self.droplet.status == 'active':
                print_log("Your droplet is active already.", "error")
            else:
                result = self.droplet.power_on()
                try:
                    if result['action']['status'] in ['in-progress','completed']:
                        print_log("Your droplet is shutdowned!", "success")
                except DropletError as err:
                    print_log(err, "error")
        else:
            print_log("Select a droplet first!", "error")

    def help_lsimages(self):
        print_log("Lists your images.", "info")

    def do_lsimages(self, line):
        if self.manager:
            images = self.manager.get_my_images() # We got problem in here
            table= []
            for image in images:
                table.append([
                    image.id, image.name, image.created_at
                ])
            headers = ['ID', 'Name','Created At']
            print_log(tabulate(table, headers, stralign="center", numalign="center", tablefmt="grid"), "success")
        else:
            print_log("Login first!", "error")

    def do_destroy(self, line):
        if self.droplet:
            destroy = False
            Break = True
            while not destroy and Break:
                sure = input("Are you sure? [y\\N]")
                if sure.lower() == "y":
                    destroy = True
                elif sure.lower() == "n":
                    Break = False
                
                    
            if destroy:
                try:
                    self.droplet.destroy()
                    print_log("Destroy initiated successfully!", "error")
                except DataReadError as err:
                    print_log(err, "error")
            else:
                print_log("Cancelled!", "info")  
        else:
            print_log("Select a droplet first!", "error")
    
    def help_newfromimage(self):
        print_log("Create a new droplet from your images.", "info")
    
    def do_newfromimage(self, image_id):
        if self.manager:
            if len(image_id) > 1:
                sizes = self.manager.get_all_sizes()
                for i,j in enumerate(sizes):
                    print("{0} - {1}, per month: ${2}".format(i, j.slug.upper(), j.price_monthly))
                print(colored("X - Exit", "red"))
                response = input("Choice:")
                if response.upper() == "X":
                    print_log("Cancelled.", "info")
                try:    
                    image = self.manager.get_image(image_id)
                    import random
                    droplet = digitalocean.Droplet(
                        token=self.uniqueKey,
                        name=image.name,
                        region=random.choice(image.regions),
                        image=image.id,
                        size_slug=sizes[int(response)].slug
                        )
                    droplet.create()
                    print_log("Droplet creation initiated successfully!", "success")
                except DataReadError as err:
                    print_log(err, "error")
            else:
                print_log("Please enter a image id!", "error")
        else:
            print_log("Login first!", "error")
            
if __name__ == "__main__":
    init()
    try:
        DigitalOcean().cmdloop()
    except KeyboardInterrupt:
        pass
