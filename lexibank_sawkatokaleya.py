import attr
import pylexibank
from clldutils.path import Path
from clldutils.misc import slug

@attr.s
class CustomLexeme(pylexibank.Lexeme):
    Category = attr.ib(default=None)

@attr.s
class CustomConcept(pylexibank.Concept):
    Category = attr.ib(default=None)

class Dataset(pylexibank.Dataset):
    dir = Path(__file__).parent
    id = "sawkatokaleya"
    lexeme_class = CustomLexeme
    concept_class = CustomConcept

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

        concepts = {}
        for concept in self.conceptlists[0].concepts.values():
            idx=concept.number + "_" + slug(concept.english)
            args.writer.add_concept(
                ID=idx,
                Category=concept.attributes['category'],
                Name=concept.english,
                Concepticon_ID=concept.concepticon_id,
                Concepticon_Gloss=concept.concepticon_gloss
            )
            concepts[concept.english] = idx

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