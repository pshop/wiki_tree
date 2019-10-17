links = {
    from: '',
    linkA:{'from': 'linkA',
           'linkB': {...},
           'linkC': {'from': 'linkC',
                     'linkX': {...},
                     'linkY': {...},
            }
           'linkD': {...}
    }
}


arbre_liens = orderedDict()

pour chaque item de la list de liens (uniques et non déjà visités, premier elem lien parent):
    arbre_lien