import click

@click.command()
def cli():
    click.echo("Congratulations! You've installed LACE framework. See documents at http://lace.readthedocs.io/")

if __name__ == '__main__':
    cli()

