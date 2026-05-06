
import jpg6
import ehen
import constants


def main():
    host_select = 0

    while host_select < 1 or host_select > len(constants.image_hosts):
        print("Select an image host:")
        
        for i, host in enumerate(constants.image_hosts):
            print(f"{i + 1}. {host}")

        host_select = int(input("\nChoose an image host: "))

    print(f"You selected: {constants.image_hosts[host_select - 1]}")

    run_type_select = 0
    while run_type_select < 1 or run_type_select > len(constants.run_type):
        print("\nSelect a run type:")
        
        for i, rtype in enumerate(constants.run_type):
            print(f"{i + 1}. {rtype}")

        run_type_select = int(input("\nChoose a run type: "))

    url = input("Enter the desired URL: ")

    match host_select:
        case 1:
            jpg6.jpg6(url).main(url, run_type_select)
        case 2:
            ehen.ehen(url).main(url, run_type_select)
        case 3:
            print("EveriaClub support coming soon!")
        case 4:
            print("bunkr support coming soon!")

main()

