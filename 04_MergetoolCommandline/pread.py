import readline
import shlex
import cmd
import pynames

classes = { 
    'scandinavian': 'scandinavian.ScandinavianNamesGenerator',
    'russian': 'russian.PaganNamesGenerator',
    'mongolian': 'mongolian.MongolianNamesGenerator',
    'korean': 'korean.KoreanNamesGenerator',
    'goblins': 'goblin.GoblinGenerator',
    'orcs': 'orc.OrcNamesGenerator'
    }

elven_subclasses = {
        'dnd': 'elven.DnDNamesGenerator',
        'warhammer': 'elven.WarhammerNamesGenerator'
    }

iron_kingdom_subclasses = {
        'caspian_midlunder_sulese': 'iron_kingdoms.CaspianMidlunderSuleseFullnameGenerator',
        'dwarf': 'iron_kingdoms.DwarfFullnameGenerator',
        'gobber': 'iron_kingdoms.GobberFullnameGenerator',
        'iossan_nyss': 'iron_kingdoms.IossanNyssFullnameGenerator',
        'khadoran': 'iron_kingdoms.KhadoranFullnameGenerator',
        'ogrun': 'iron_kingdoms.OgrunFullnameGenerator',
        'ryn': 'iron_kingdoms.RynFullnameGenerator',
        'thurian_morridane': 'iron_kingdoms.ThurianMorridaneFullnameGenerator',
        'morridane': 'iron_kingdoms.MorridaneFullnameGenerator',
        'thurian': 'iron_kingdoms.ThurianFullnameGenerator',
        'tordoran': 'iron_kingdoms.TordoranFullnameGenerator',
        'trollkin': 'iron_kingdoms.TrollkinFullnameGenerator' 
    }

all_names = {**classes, **elven_subclasses, **iron_kingdom_subclasses}

def completion_list(prefix, source):
    return [s for s in source if s.startswith(prefix)]

class repl(cmd.Cmd):
    prompt = "> "
    language = 'native'

    def print_name(self, cls, gender='m'):
        try:
            print(eval(f'pynames.generators.{classes[cls]}().get_name_simple("{gender}", "{self.language}")'))
        except KeyError:
            print(eval(f'pynames.generators.{classes[cls]}().get_name_simple("{gender}", "native")'))
    
    def print_elven_name(self, subcls='dnd', gender='m'):
        try:
            print(eval(f'pynames.generators.{elven_subclasses[subcls]}().get_name_simple("{gender}", "{self.language}")'))
        except KeyError:
            print(eval(f'pynames.generators.{elven_subclasses[subcls]}().get_name_simple("{gender}", "native")'))

    def print_iron_kingdom_name(self, subcls='caspian_midlunder_sulese', gender='m'):
        try:
            print(eval(f'pynames.generators.{iron_kingdom_subclasses[subcls]}().get_name_simple("{gender}", "{self.language}")'))
        except Exception as e:
            print(eval(f'pynames.generators.{iron_kingdom_subclasses[subcls]}().get_name_simple("{gender}", "native")'))


    def do_generate(self, arg):
        """
Variants:
        perform show argws
        perform sing args
        """
        args = shlex.split(arg, comments=True)
        if args[0].lower() in classes:
            if len(args) == 1:
                self.print_name(args[0].lower())
            elif len(args) == 2:
                self.print_name(args[0].lower(), gender=args[1].lower()[0])
        elif args[0].lower() == 'elven':
            if len(args) == 1:
                self.print_elven_name()
            elif len(args) == 2 and args[1].lower() in ('male', 'female'):
                self.print_elven_name(gender=args[1].lower()[0])
            elif len(args) == 2 and args[1].lower() in elven_subclasses:
                self.print_elven_name(subcls = args[1].lower())
            elif len(args) == 3:
                self.print_elven_name(subcls=args[1].lower(), gender=args[2].lower()[0])
        elif args[0].lower() == 'iron_kingdoms':
            if len(args) == 1:
                self.print_iron_kingdom_name()
            elif len(args) == 2 and args[1].lower() in ('male', 'female'):
                self.print_iron_kingdom_name(gender=args[1].lower()[0])
            elif len(args) == 2 and args[1].lower() in iron_kingdom_subclasses:
                self.print_iron_kingdom_name(subcls = args[1].lower())
            elif len(args) == 3:
                self.print_iron_kingdom_name(subcls=args[1].lower(), gender=args[2].lower()[0])
            
    def do_language(self, arg):
        args = shlex.split(arg, comments=True)
        if len(args) == 1:
            if args[0].lower() in ('en', 'ru'):
                self.language = args[0].lower()

    def do_info(self, arg):
        args = shlex.split(arg, comments=True)
        if len(args) == 1 and args[0].lower() in all_names:
            print(eval(f'pynames.generators.{all_names[args[0].lower()]}().get_names_number()'))
        elif len(args) == 2 and args[0].lower() in all_names:
            if args[1].lower() in ('male', 'female'):
                gender = args[1].lower()[0]
                print(eval(f'pynames.generators.{all_names[args[0].lower()]}().get_names_number("{gender}")'))
            elif args[1].lower() == 'language':
                langs = list(eval(f'pynames.generators.{all_names[args[0].lower()]}().get_name().translations["m"].keys()'))
                print(*sorted([lang for lang in langs if lang in ['en', 'ru']]))
                

    def complete_generate(self, prefix, allcommand, beg, end):
        if allcommand.count(' ') == 1:
            return completion_list(prefix, list(classes) + ['elven', 'iron_kingdoms'] + [s.title() for s in list(classes) + ['elven', 'iron_kingdoms']])
        elif allcommand.count(' ') == 2:
            first = allcommand.split()[1].lower()
            if first in classes:
                return completion_list(prefix, ['male', 'female'])
            elif first == 'elven':
                return completion_list(prefix, list(elven_subclasses) + [s.title() for s in elven_subclasses])
            elif first == 'iron_kingdoms':
                return completion_list(prefix, list(iron_kingdom_subclasses) + [s.title() for s in iron_kingdom_subclasses])
        elif allcommand.count(' ') == 3:
            first = allcommand.split()[1].lower()
            if first in ('elven', 'iron_kingdoms'):
                return completion_list(prefix, ['male', 'female'])

    def complete_info(self, prefix, allcommand, beg, end):
        if allcommand.count(' ') == 1:
            return completion_list(prefix, all_names)
        elif allcommand.count(' ') == 2:
            first = allcommand.split()[1].lower()
            if first in all_names:
                return completion_list(prefix, ['male', 'female', 'language'])
 
    def complete_language(self, prefix, allcommand, beg, end):
        if allcommand.count(' ') == 1:
            return completion_list(prefix, ['en', 'ru', 'EN', 'RU'])

    def do_e(self, arg):
        """Exit command line"""
        return True

repl().cmdloop()
