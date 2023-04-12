def vetor_solar(date):

    """
    :param date: date of interest
    :return: solar vector
    """
    from datetime import datetime
    import numpy as np
    def utc_to_jd(date):
        # separa a string data
        dt = date

        # converte datetime para tempo juliano
        a = (14 - dt.month) // 12
        y = dt.year + 4800 - a
        m = dt.month + 12 * a - 3
        jd = dt.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045

        # adiciona fração do dia
        frac_day = (dt.hour - 12) / 24.0 + dt.minute / 1440.0 + dt.second / 86400.0
        jd += frac_day

        return jd

    # calcula a data juliana para hoje
    data = datetime(month= date.month, day= date.day, year=date.year, hour=date.hour, minute=date.minute)

    # calcula o século juliano
    T_uti = (utc_to_jd(data) - 2451545.0) / 36525

    T_tdb = T_uti

    # calcula a longitude média do sol
    lamb_M = (280.46 + 36000.771 * T_tdb) % 360

    # anomalia media para o sol
    M_sol = (357.5291092 + 35999.05034*T_tdb)% 360


    # calcula a longitude da ecliptica
    lamb_ecl = lamb_M + 1.914666471 * np.sin(np.radians(M_sol)) + 0.019994643 * np.sin(np.radians(2 * M_sol))

    # calcula a obliquidade da ecliptica
    e = 23.439291 - 0.0130042*T_tdb

    # magnitude da distancia do sol
    r_sol = 1.000140612 - 0.016708617 * np.cos(np.radians(M_sol)) - 0.000139589 * np.cos(np.radians(2 * M_sol))

    # vetor posicao solar
    r_sol_vet = [r_sol * np.cos(np.radians(lamb_ecl)), r_sol * np.cos(np.radians(e)) * np.sin(np.radians(lamb_ecl)),
                 r_sol * np.sin(np.radians(e)) * np.sin(np.radians(lamb_ecl))]
    vet_sol = [x * 149597870.7 for x in r_sol_vet]
    return vet_sol

if __name__ == '__main__':
    from datetime import datetime
    import numpy as np
    input_string = '04/05/2023 16:00:00'
    data = datetime.strptime(input_string, "%m/%d/%Y %H:%M:%S")
    a = vetor_solar(data)
    vetor_solar_normalizado = [x / np.linalg.norm(a) for x in a]
    print(vetor_solar(data))
    print(f'vetor solar normalizado : {vetor_solar_normalizado}')
    from datetime import timedelta
    b = [data + timedelta(days=x) for x in range(0,365)]
    print(b)
    vetor_solar_anual = [vetor_solar(x) for x in b]
    print(vetor_solar_anual)

    import pandas as pd
    df = pd.DataFrame(vetor_solar_anual, columns=['X_sun', 'Y_sun', 'Z_sun'])
    lat = lambda row: np.degrees(np.arcsin(row[2] / np.linalg.norm(row)))
    long = lambda row: np.degrees(np.arctan2(row[1], row[0]))
    df['latitude'] = np.degrees(np.arcsin(df['Z_sun'] / np.linalg.norm([df['X_sun'], df['Y_sun'], df['Z_sun']])))   #df.apply(lat, axis=1)
    df['longitude'] = np.degrees(np.arctan2(df['Y_sun'], df['X_sun']))  #df.apply(long, axis=1)
    print(df)

    import plotly.express as px

    fig = px.scatter_geo(data_frame=df, lat = 'latitude', lon = 'longitude')
    fig.show()
