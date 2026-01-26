from functions import prepare_public, generate_pages_recursive


def main():
    prepare_public()
    generate_pages_recursive("content", "template.html", "public")

main()
