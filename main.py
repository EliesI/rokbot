def main():
    print("Sélectionnez une action :")
    print("1. Récolte de gemmes")
    print("2. Récolte de fermes (à venir)")
    print("3. Chasse barbares (à venir)")
    print("4. Aide à l'alliance (a)")
    print("3. Chasse barbares (à venir)")
    choix = input("Votre choix : ")

    if choix == "1":
        from actions.gems import farming_gem_loop
        farming_gem_loop()

    elif choix == "2":
        print("Fonctionnalité de récolte de fermes à venir.") 
    elif choix == "3":
        print("Fonctionnalité de chasse aux barbares à venir.")
    elif choix == "q":
        print("Quitter le programme.")
        return
    elif choix == "a":
        from actions.alliance import help_alliance
        help_alliance()
    # Ajoute d'autres actions ici

if __name__ == "__main__":
    main()

