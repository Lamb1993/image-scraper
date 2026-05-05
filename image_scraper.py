
import jpg6
import ehen

image_hosts = ['jpg6', 'bunkr']
run_type = ["html", "images"]

def main():
    host_select = 0

    while host_select < 1 or host_select > len(image_hosts):
        print("Select an image host:")
        
        for i, host in enumerate(image_hosts):
            print(f"{i + 1}. {host}")

        host_select = int(input("\nChoose an image host: "))

    print(f"You selected: {image_hosts[host_select - 1]}")

    run_type_select = 0
    while run_type_select < 1 or run_type_select > len(run_type):
        print("\nSelect a run type:")
        
        for i, rtype in enumerate(run_type):
            print(f"{i + 1}. {rtype}")

        run_type_select = int(input("\nChoose a run type: "))

    url = input("Enter the desired URL: ")

    match host_select:
        case 1:
            jpg6.jpg6(url).main(url, run_type_select)
        case 2:
            print("bunkr support coming soon!")

main()
