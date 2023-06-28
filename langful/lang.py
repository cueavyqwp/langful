"""
# lang
"""
from locale import getdefaultlocale
import json
import os

def lang_to_json( lang_file : str ) -> dict :
    """
    .lang -> .json
    """
    ret = {}
    for i in lang_file.split( "\n" ) :
        text = i.split("#")[0]
        line = "".join( text.split( maxsplit = 2 ) )
        if line :
            key_value = i.split( "=" , 1 )
            if len( key_value ) == 2 :
                key , value = i.split( "=" , 1 )
            else :
                raise SyntaxError( "can't to read .lang file" )
            ret[ key ] = value
    return ret

def json_to_lang( dict_file : dict ) -> str :
    """
    .json -> .lang
    """
    ret = ""
    for key , value in dict_file.items() :
        if not ( isinstance( value , int ) or isinstance( value , str ) ) :
            raise TypeError( f"can't use type '{ type( value ) }'" )
        ret += f"{ key } = { value }\n"
    return ret

class lang :
    """
    # lang
    """
    def __init__( self , lang_dir : str  |  bool = "lang" , default_locale : str = "en_us" ) -> None :
        """
        lang_dir: lang files dir, if use dict to set that False
        default_locale: default locale
        """
        self.lang_dir = lang_dir
        system_locale = self.get_system_locale
        self.default_locale = default_locale
        self.system_locale = system_locale
        self.replace_letter = "%"
        self.is_file = False
        self.languages = {}
        self.locales = []
        self.types = {}
        self.init()

    def init( self ) -> None :
        """
        # init
        """
        path = self.lang_dir
        if isinstance( path , str ) :
            self.is_file = True
        if self.is_file :
            if not os.path.exists( path ) :
                raise FileNotFoundError( f"can't find '{ os.path.abspath( path ) }'" )
            files = []
            for i in os.listdir( path ) :
                name , suffix = os.path.splitext( i )
                if ( suffix == ".json" ) or ( name + ".json" not in files ) :
                    files.append( i )
                    with open( os.path.join( path , i ) , encoding = "utf-8" ) as file :
                        if suffix == ".json" :
                            try :
                                data = json.load( file )
                            except json.decoder.JSONDecodeError :
                                raise SyntaxError( "can't to load .json file" )
                        elif suffix == ".lang" :
                            data = lang_to_json( file.read() )
                        else :
                            continue
                    self.locales.append( name )
                    self.languages[ name ] = data
                    self.types[ name ] = suffix

    def init_dict( self , language : dict ) -> None :
        """
        init by a dictionary, but cant't to save
        """
        if self.is_file :
            raise TypeError( "can't init by a dictionary, because it's init by a dir" )
        for value in language.values() :
            if not isinstance( value , dict ) :
                raise TypeError( f"can't use type '{ type( value ) }'" )
        for key in language.keys() :
            self.types[ key ] = ".json"
            self.locales.append( key )
        self.languages = language

    @property
    def get_system_locale( self ) -> str :
        """
        get system locale
        """
        return getdefaultlocale()[0].lower() # 系统语言

    @property
    def locale( self ) -> str :
        """
        choose locale
        """
        if self.system_locale in self.locales :
            return self.system_locale
        elif self.default_locale in self.locales :
            return self.default_locale
        else :
            raise KeyError( f"no such locale '{ self.system_locale }' or '{ self.default_locale }'" )

    @property
    def language( self ) -> dict :
        """
        get now language
        """
        return self.languages[ self.locale ]

    @property
    def lang( self ) -> dict :
        """
        same to language function
        """
        return self.language

    @property
    def type( self ) -> str :
        """
        get type, '.json' or '.lang'
        """
        return self.types[ self.locale ]

    def get_locale( self , locale : str = None ) -> str :
        if locale :
            return locale
        else :
            return self.locale

    def get_replace_letter( self , replace_letter : str = None ) -> str :
        if replace_letter :
            return replace_letter
        else :
            return self.replace_letter

    def set_locale( self , locale : str = None  ) -> None :
        """
        set/reset locale
        """
        if locale != None :
            self.system_locale = locale
        else :
            self.system_locale = self.get_system_locale

    def lang_set( self , locale : str , suffix : str , value : dict = {} ) -> None :
        """
        set lang
        """
        self.languages[ locale ] = value
        self.types[ locale ] = suffix

    def lang_del( self , locale : str ) -> None :
        """
        del lang
        """
        del self.languages[ locale ]
        del self.types[ locale ]

    def get( self , key : str | int , locale : str = None ) -> str :
        """
        get
        """
        locale = self.get_locale( locale )
        return self.languages[ locale ][ key ]

    def set( self , key : str | int , value : str , locale : str = None ) -> None :
        """
        set
        """
        locale = self.get_locale( locale )
        self.languages[ locale ][ key ] = value

    def remove( self , key : str | int , locale : str = None ) -> None :
        """
        remove
        """
        locale = self.get_locale( locale )
        del self.languages[ locale ][ key ]

    def save( self ) -> None :
        """
        save file, when is_file is true
        """
        if self.is_file :
            for key , value in self.languages.items() :
                suffix = self.types[ key ]
                print(suffix,value)
                with open( os.path.join( self.lang_dir , key + suffix ) , "w+" , encoding = "utf-8" ) as file :
                    if suffix == ".json" :
                        file.write( json.dumps( value , indent = 4 , separators = ( " ," , ": " ) , ensure_ascii = False ) )
                    elif suffix == ".lang" :
                        file.write( json_to_lang( value ) )
        else :
            raise TypeError( "can't to save, because it's not a file" )

    def save_dict( self ) -> dict :
        """
        save dict. in fact, it just return the 'languages' variable
        """
        if not self.is_file :
            return self.languages
        else :
            raise TypeError( "can't to save, because it's not a dict" )

    def replace( self , key : str = None , args : list | str = None , locale : str = None , replace_letter : str = None ) -> str :
        """
        replace
        """
        # locale = self.get_locale( locale )
        # replace_letter = self.get_replace_letter( replace_letter )
        # text = []
        # ret = ""
        # p = 0
        # for i in self.get( key ).split( replace_letter * 2 ) :
        #     if i :
        #         print(i.split( replace_letter ))
        #         text += i.split( replace_letter )
        #     else :
        #         text += replace_letter
        # print(text)
        # if not isinstance( args , list ) :
        #     args = [ str( args ) ]
        # for i in range ( len( text ) ) :
        #     print(text[i])
        #     p += 1
        # return ret
        if not replace_letter :
            replace_letter = self.replace_letter
        if not locale :
            locale = self.locale
        text = self.get( key , locale ).split( replace_letter )
        if len( text ) == 1 :
            text = text[0]
        ret = ""
        for i in range( len( text ) ) :
            if ( len( text ) - 1 ) > i :
                if len( args ) > i :
                    ret += text[i] + args[i]
                else :
                    ret += text[i] + args[-1]
            else :
                ret += text[i]
        return ret

    def replace_str( self , text : str , locale : str = None , replace_letter : str = None ) -> str :
        """
        replace by str
        """
        locale = self.get_locale( locale )
        replace_letter = self.get_replace_letter( replace_letter )
        text = text.split( replace_letter )
        ret = ""
        p = 0
        for i in text :
            if p % 2 :
                if i :
                    ret += self.get( i )
                else :
                    ret += replace_letter
            else :
                ret += i
            p += 1
        return ret
