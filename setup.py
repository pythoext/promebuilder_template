import os
import shutil
import sys
import six
from promebuilder import gen_metadata, setup

METADATA = gen_metadata(
    name="promebuilder_template",
    description="Promebuilder Template Project",
    email="pytho_support@prometeia.com",
    keywords="prometeia template project pipeline jenkins",
)


if __name__ == '__main__':
    setup(METADATA)
    # Don't mess with STDOUT, il would parsed by jenkins to discover package name!
    old_stdout = sys.stdout
    sys.stdout = mystdout = six.StringIO()
    doc_final_path = os.path.join("dist", "doc", METADATA["name"], METADATA["version"])
    try:
        from pdoc.cli import main, parser

        print("INFO: Generating doc in {}".format(doc_final_path))
        params = "-o {} --html --template-dir template_dir {} --force".format(
            os.path.join("dist", "doc", METADATA["name"]), METADATA["name"]).split()
        main(parser.parse_args(params))
        if os.path.isdir(doc_final_path):
            shutil.rmtree(doc_final_path)
        os.rename(os.path.join("dist", "doc", METADATA["name"], METADATA["name"]), doc_final_path)
        print("INFO: Doc entrypoint is {}".format(os.path.join(doc_final_path, "index.html")))
    except ImportError:
        print("WARNING: Cannot import pdoc3, skipping doc generation")
    finally:
        sys.stdout = old_stdout
        print(mystdout.getvalue(), file=sys.stderr)
