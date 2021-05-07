from glossary import GlossaryChecker

if __name__=='__main__':
    import glob
    gc = GlossaryChecker(
        glob.glob('./pyxliff/tests/testdata/*.sdlxliff')[0],
        './pyxliff/tests/testdata/excel_glossary.xlsx'
    )
    gc.check()
    print(gc.segments[0].source)

# Why is the importing of glossary not working if shift+enter?