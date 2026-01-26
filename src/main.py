from functions import prepare_public, generate_page


def main():
    prepare_public()
    generate_page("content/index.md", "template.html", "public/index.html")

main()
