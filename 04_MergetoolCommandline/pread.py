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
        'dnd': 'DnDNamesGenerator',
        'warhammer': 'WarhammerNamesGenerator'
    }

iron_kingdom_subclasses = {
        'caspian midlunder sulese': 'CaspianMidlunderSuleseFullnameGenerator',
        'dwarf': 'DwarfFullnameGenerator',
        'gobber': 'GobberFullnameGenerator',
        'iossan nyss': 'IossanNyssFullnameGenerator',
        'khadoran': 'KhadoranFullnameGenerator',
        'ogrun': 'OgrunFullnameGenerator',
        'ryn': 'RynFullnameGenerator',
        'thurian morridane': 'ThurianMorridaneFullnameGenerator',
        'morridane': 'MorridaneFullnameGenerator',
        'thurian': 'ThurianFullnameGenerator',
        'tordoran': 'TordoranFullnameGenerator',
        'trollkin': 'TrollkinFullnameGenerator' 
    }

def completion_list(prefix, source):
    return [s for s in source if s.startswith(prefix)]

class repl(cmd.Cmd):
    prompt = "> "
    language = 'native'

    def print_name(self, cls, gender='m'):
        try:
            print(eval(f'pynames.generators.{classes[cls]}.get_name_simple("{gender}", "{self.language}")'))
        except KeyError:
            print(eval(f'pynames.generators.{classes[cls]}.get_name_simple("{gender}", "native")'))
    
    def print_elven_name(self, subcls='dnd', gender='m'):
        try:
            print(eval(f'pynames.generators.elven.{elven_subclasses[subcls]}().get_name_simple("{gender}", "{self.language}")'))
        except KeyError:
            print(eval(f'pynames.generators.elven.{elven_subclasses[subcls]}.get_name_simple("{gender}", "native")'))

    def print_iron_kingdom_name(self, subcls='caspian midlunder sulese', gender='m'):
        try:
            print(eval(f'pynames.generators.iron_kingdoms.{iron_kingdom_subclasses[subcls]}.get_name_simple("{gender}", "{self.language}")'))
        except KeyError:
            print(eval(f'pynames.generators.iron_kingdoms.{iron_kingdom_subclasses[subcls]}.get_name_simple("{gender}", "native")'))


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
                self.print_names(args[0], gender=args[1].lower()[0])
        elif args[0].lower() == 'elven':
            if len(args) == 1:
                self.print_elven_name()
            elif len(args) == 2 and args[1].lower() in ('male', 'female'):
                self.print_elven_name(gender=args[1].lower()[0])
            elif len(args) == 2 and args[1].lower() in elven_subclasses:
                self.print_elven_name(subcls = args[1].lower())
            elif len(args) == 3:
                self.print_elven_name(subcls=args[1].lower(), gender=args[2].lower()[0])
        elif args[0].lower == 'iron_kingdoms':
            if len(args) == 1:
                self.print_iron_kingdom_name()
            elif len(args) == 2 and args[1].lower() in ('male', 'female'):
                self.print_iron_kingdom_name(gender=args[1].lower()[0])
            elif len(args) == 2 and args[1].lower() in elven_subclasses:
                self.print_irom_kingdom_name(subcls = args[1].lower())
            elif len(args) == 3:
                self.print_iron_kingdom_name(subcls=args[1].lower(), gender=args[2].lower()[0])
            

    def complete_generate(self, prefix, allcommand, beg, end):
        if allcommand.count(' ') == 1:
            a = 3
            return completion_list(prefix, list(classes) + ['elven', 'iron_kingdoms'])
        elif allcommand.count(' ') == 2:
            first = allcommand.split()[1]
            if first in classes:
                return completion_list(prefix, ['male', 'female'])
            elif first == 'elven':
                return completion_list(prefix, list(elven_subclasses))
            elif first == 'iron_kingdoms':
                return completion_list(prefix, list(iron_kingdom_subclasses))
        elif allcommand.count(' ') == 3:
            first = prefix.split()[1]
            if first in ('elven', 'iron_kingdoms'):
                return completion_list(prefix, ['male', 'female'])


    def do_e(self, arg):
        """Exit command line"""
        return True

repl().cmdloop()
