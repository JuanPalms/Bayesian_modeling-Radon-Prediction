
    data {
        int<lower=1> N;  // observations
        int<lower=1> J;  // counties
        array[N] int<lower=1, upper=J> county;
        vector[N] x;     // floor
        vector[N] y;     // radon
    }
    parameters {
        vector[J] alpha;
        real beta;
        real<lower=0> sigma;
    }
    model {
        y ~ normal(alpha[county] + beta * x, sigma);  
        alpha ~ normal(1, 1);
        beta ~ normal(0, 1);
        sigma ~ normal(0, 1);
    }
    generated quantities {
        array[N] real y_rep = normal_rng(alpha[county] + beta * x, sigma);
        array[N] real log_lik;
        for (n in 1:N)
            log_lik[n] = normal_lpdf(y[n] | alpha[county[n]] + beta * x[n], sigma);
    }
