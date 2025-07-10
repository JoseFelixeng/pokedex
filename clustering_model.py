def gerar_csv_com_clusters():
    import pandas as pd
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    import joblib
    import os

    # Carregar dataset original
    df = pd.read_csv("pokemon.csv")

    # Selecionar atributos usados no clustering
    features = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
    X = df[features]

    # Normalizar atributos
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Treinar KMeans
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    clusters_novos = kmeans.fit_predict(X_scaled)

    df['Cluster'] = clusters_novos

    # Mapear Cluster para Perfil
    cluster_labels = {
        0: "Atacante",
        1: "Tanque",
        2: "Rápido",
        3: "Balanceado"
    }
    df['Perfil Oculto'] = df['Cluster'].map(cluster_labels)

    # Verificar se o arquivo já existe
    arquivo_existente = "pokemon_com_perfil.csv"
    precisa_salvar = True

    if os.path.exists(arquivo_existente):
        df_existente = pd.read_csv(arquivo_existente)

        if 'Cluster' in df_existente.columns and df_existente['Cluster'].equals(df['Cluster']):
            #print("Os clusters não mudaram. Arquivo não será sobrescrito.")
            precisa_salvar = False

    if precisa_salvar:
        df.to_csv(arquivo_existente, index=False)
        joblib.dump(kmeans, "modelo_kmeans.pkl")
        joblib.dump(scaler, "scaler_kmeans.pkl")
        print("Clusters atualizados e arquivos salvos.")