import attr
import pylexibank
from clldutils.path import Path
from clldutils.misc import slug

@attr.s
class CustomLexeme(pylexibank.Lexeme):
    Category = attr.ib(default=None)


class Dataset(pylexibank.Dataset):
    dir = Path(__file__).parent
    id = "sawkatokaleya"
    lexeme_class = CustomLexeme

    form_spec = pylexibank.FormSpec(
        brackets={"(": ")", "[": "]"},
        separators="/",
        missing_data=('', ' '),
        strip_inside_brackets=True
    )

    def cmd_makecldf(self, args):
        data = self.raw_dir.read_csv('raw.csv', dicts=True)
        args.writer.add_sources()
        languages = args.writer.add_languages(lookup_factory="Name")
        concepts = args.writer.add_concepts(
        	id_factory=lambda c: c.number + "_" + slug(c.english), lookup_factory="Name"
        	)
        
        for row in pylexibank.progressbar(data):
        	for language, lexeme in row.items():
        		if language in languages:
        			args.writer.add_forms_from_value(
        				Language_ID=languages[language],
                        Parameter_ID=concepts[row["English"]],
                        Value=lexeme,
                        Category=row["Category"],
                        Source="Sawka2019",
                    )