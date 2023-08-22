
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
        real mu_beta;
        real<lower=0> sigma_beta;
        vector<offset=mu_beta, multiplier=sigma_beta>[J] beta; // non-centered parameterization
        real<lower=0> sigma;
    }
    model {
        y ~ normal(alpha[county] + beta[county] .* x, sigma);
        alpha ~ normal(mu_alpha, sigma_alpha); // partial-pooling
        beta ~ normal(mu_beta, sigma_beta); // partial-pooling
        mu_alpha ~ normal(1, 1);
        sigma_alpha ~ normal(0, 1);
        mu_beta ~ normal(0, 1);
        sigma_beta ~ normal(0, 1);
        sigma ~ normal(0, 1);
    }
    generated quantities {
        array[N] real y_rep;
        array[N] real log_lik;
        
        for (i in 1:N) {
            y_rep[i] = normal_rng(alpha[county[i]] + beta[county[i]] * x[i], sigma);
            log_lik[i] = normal_lpdf(y[i] | alpha[county[i]] + beta[county[i]] * x[i], sigma);
        }
    }
