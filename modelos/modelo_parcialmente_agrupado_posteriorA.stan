
    data {
        int<lower=1> N;  // observations
        int<lower=1> J;  // counties
        array[N] int<lower=1, upper=J> county;
        vector[N] x;
        vector[N] y;
    }
    parameters {
        real mu_alpha;
        real<lower=0> sigma_alpha;
        vector<offset=mu_alpha, multiplier=sigma_alpha>[J] alpha;  // non-centered parameterization
        real beta;
        real<lower=0> sigma;
    }
    model {
        y ~ normal(alpha[county] + beta * x, sigma);  
        alpha ~ normal(mu_alpha, sigma_alpha); // partial-pooling
        beta ~ normal(0, 1);
        sigma ~ normal(0, 1);
        mu_alpha ~ normal(1, 1);
        sigma_alpha ~ normal(0, 1);
    }
    generated quantities {
        array[N] real y_rep = normal_rng(alpha[county] + beta * x, sigma);
        array[N] real log_lik;
        for (n in 1:N)
            log_lik[n] = normal_lpdf(y[n] | alpha[county[n]] + beta * x[n], sigma);
    }
