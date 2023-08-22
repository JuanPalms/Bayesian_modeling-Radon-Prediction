data {
    // Número de partidos
    int<lower=1> n_matches;
    // Número de regiones
    int<lower=0> n_regiones;
    // Goles por equipo
    array[n_matches] int <lower=0> goals_home;
    array[n_matches] int <lower=0> goals_away;

    array[n_regiones] int <lower=0, upper=n_regiones> regiones;
}

parameters {
    // Habilidad por equipo <offset= mu_bl, multiplier=sigma_bl>
    real mu_bl;
    real sigma_bl;
    array[n_matches, n_regiones] real baseline;
    array[n_matches] real skill_home;
    array[n_matches] real skill_away;
    real mu_teams;
    real sigma_teams;
}

transformed parameters {
    // Media de distribuciones
    array[n_matches] real <lower=0> lambda_home;
    array[n_matches] real <lower=0> lambda_away;

    for (match in 1:n_matches)
        for(region in 1:n_regiones)
            lambda_home[match] = exp(baseline[match,region] + skill_home[match] - skill_away[match]);
    
    for (match in 1:n_matches)
        for (region in 1:n_regiones)
            lambda_away[match] = exp(baseline[match,region] + skill_away[match] - skill_home[match]);
}

model {
    // Modelo de goles anotados
    goals_home ~ poisson(lambda_home);
    goals_away ~ poisson(lambda_away);
    // Modelo de habilidad por equipo
    skill_home ~ normal(mu_teams, sigma_teams);
    skill_away ~ normal(mu_teams, sigma_teams);
    // Parámetros de habilidad
    mu_teams ~ normal(0, 4);
    sigma_teams ~ gamma(5, 5);
    //
    mu_bl ~ normal(0, 4);
    sigma_bl ~ gamma(5, 5);
}

generated quantities {
    array[n_matches] real sims_home = poisson_rng(lambda_home);
    array[n_matches] real sims_away = poisson_rng(lambda_away);
}
