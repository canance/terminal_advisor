import argparse
import getpass
import configparser
import keyring
import os
import sys
import os.path
from terminal_advisor.advisor import Advisor


def parse_config(args, config_path=['config.ini', os.path.join(os.path.expanduser('~'), '.terminal_advisor', 'config.ini')]):
    """ Setup configuration for program.  This function will also read or create a configuration file. """
    config = configparser.ConfigParser()
    if not isinstance(config_path, list):
        config_path = [config_path]
    for path in config_path:
        if os.path.isfile(path):
            config.read(path)
            break
    if len(config.sections()) == 0:  # make config
        config['DEFAULT'] = {
            'User': '',
            'WebadvisorURL': '',
            'Driver': '',
        }
        config['KEYRING'] = {
            'Use': 'false',
            'Keychain': 'terminaladvisor-webadvisor',
        }

    if args.user is not None:
        config['DEFAULT']['User'] = args.user
    if args.base_url is not None:
        config['DEFAULT']['WebadvisorURL'] = args.base_url
    if args.driver is not None:
        config['DEFAULT']['Driver'] = args.driver

    if not config['DEFAULT']['User']:
        config['DEFAULT']['User'] = input('Username: ')

    password = ''
    if config.getboolean('KEYRING', 'Use'):
        password = keyring.get_password(config['KEYRING']['Keychain'], config['DEFAULT']['User'])
    if not password and not args.gui:
        password = getpass.getpass('Password: ')
        store = input("Would you like to store this password in your keychain (Y/n): ")
        if store.lower() in ['y', 'yes', '']:
            config['KEYRING']['Use'] = 'true'
            keyring.set_password(config['KEYRING']['Keychain'], config['DEFAULT']['User'], password)
    
    if not config['DEFAULT']['WebadvisorURL']:
        config['DEFAULT']['WebadvisorURL'] = input('Webadvisor base URL: ')
    
    if not config['DEFAULT']['Driver']:
        config['DEFAULT']['Driver'] = 'PhantomJS'
    
    if args.save_config:
        save = input('Save configuration (Y/n)? ')
        if save.lower() in ['y', 'yes', '']:
            ask_path = input('Location (%s): ' % path)
            if ask_path.strip() != '':
                path = ask_path
            if not os.path.exists(os.path.split(path)[0]):
                os.mkdir(os.path.split(path)[0])
            with open(path, 'w') as configfile:
                config.write(configfile)

    return (config, password)


def get_args():
    """ Parse command line arguments. """
    drivers = ['PhantomJS', 'Chrome']
    parser = argparse.ArgumentParser(description='Automate mundane tasks in Webadvisor')
    parser.add_argument('--user', dest='user', help='User name to log in to webadvisor')
    parser.add_argument('--base-url', dest='base_url', help='Base URL for webadvisor.  Example: https://wa.xyz.edu/')
    parser.add_argument('--config', dest='config', help='Path to a configuration file')
    parser.add_argument('--driver', dest='driver', choices=drivers, nargs='?', default='PhantomJS', help='Webdriver to use with Selenium'),
    parser.add_argument('-s', '--save-config', dest='save_config', action='store_true', help='Save configuration file')
    parser.add_argument('-r', '--remove-hold', dest='remove_hold', action='store_true', help='Remove the advisement hold')
    parser.add_argument('-e', '--program-eval', dest='prog_eval', action='store_true', help='Run a program evaluation')
    parser.add_argument('advisee', nargs='?', help="An advisee's name or a substring of the advisee's name.")
    parser.add_argument('--gui', dest='gui', action='store_true', help='Run in GUI mode.')
    parser.add_argument('--no-login', dest='no_login', action='store_true', help="This option is only used with --gui.  It tells the GUI not to login on startup.")
    return parser.parse_args()


def main():
    """ Main function.  Parse command-line arguments, load configuration, process commands. """
    args = get_args()
    config, password = parse_config(args)

    advisor = Advisor(config['DEFAULT']['WebadvisorURL'], config['DEFAULT']['user'], password, config['DEFAULT']['Driver'])

    if args.gui:
        from terminal_advisor.gui import main
        main.main(advisor, args.no_login, config)
        sys.exit(0)

    advisor.login()
    if args.advisee is not None:
        advisee = args.advisee
    else:
        advisee = input('Advisee: ')

    if args.remove_hold:
        advisor.remove_advisor_hold(advisee)
    elif args.prog_eval:
        advisor.run_program_evaluation(advisee)
    else:    
        print('1. Remove Advisor Hold')
        print('2. Run Program Evaluation')
        print('3. List Advisees')
        print('4. Quit')
        selection = -1
        while selection not in range(1, 5):
            selection = int(input('Choice: '))
        if selection == 1:
            advisor.remove_advisor_hold(advisee)
        elif selection == 2:
            advisor.run_program_evaluation(advisee)
        elif selection == 3:
            print(advisor.list_advisees())
        elif selection == 4:
            sys.exit(0)


if __name__ == '__main__':
    main()
