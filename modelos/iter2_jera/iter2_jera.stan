data {
    // Número de partidos
    int<lower=1> n_matches;
    // Goles por equipo
    array[n_matches] int <lower=0> goals_home;
    array[n_matches] int <lower=0> goals_away;
}

parameters {
    // Habilidad por equipo
    array[n_matches] real baseline;
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
        lambda_home[match] = exp(baseline[match] + skill_home[match] - skill_away[match]);
    
    for (match in 1:n_matches)
        lambda_away[match] = exp(baseline[match] + skill_away[match] - skill_home[match]);
}

model {
    // Modelo de goles anotados
    goals_home ~ poisson(lambda_home);
    goals_away ~ poisson(lambda_away);
    // Modelo de habilidad por equipo
    skill_home ~ normal(mu_teams, sigma_teams);
    skill_away ~ normal(mu_teams, sigma_teams);
    // Parámetros de habilidad
    baseline ~ normal(0, 4);
    mu_teams ~ normal(0, 4);
    sigma_teams ~ gamma(5, 5);
}

generated quantities {
    array[n_matches] real sims_home = poisson_rng(lambda_home);
    array[n_matches] real sims_away = poisson_rng(lambda_away);
}
