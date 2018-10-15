

def main(
        user: ("Username for logging through ssh", 'option', 'u'),
        interface: ("Name of Django app including FrontEnd written in webpack",
                    'option', 'i'),
):
    print("Q-Deploy. Django deployment")
    git = input('Git repo URL')


if __name__ == '__main__':
    import plac
    plac.call(main)
