from sys import argv

from functions import prepare_public, generate_pages_recursive


def main():
    basepath = argv[1]
    if not basepath:
        basepath = "/"

    pub_dir = "docs"
    prepare_public(pub_dir)
    generate_pages_recursive("content", "template.html", pub_dir, basepath)

main()
