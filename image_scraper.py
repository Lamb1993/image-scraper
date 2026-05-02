
import jpg6


image_hosts = ['jpg6', 'bunkr']


def main():
    host_select = 0

    while host_select < 1 or host_select > len(image_hosts):
        print("Select an image host:")
        
        for i, host in enumerate(image_hosts):
            print(f"{i + 1}. {host}")

        host_select = int(input("\nEnter the number corresponding to the image host: "))

    print(f"You selected: {image_hosts[host_select - 1]}")

    url = input("Enter the desired URL: ")

    match host_select:
        case 1:
            jpg6.jpg6(url).main(url)
        case 2:
            print("bunkr support coming soon!")

main()