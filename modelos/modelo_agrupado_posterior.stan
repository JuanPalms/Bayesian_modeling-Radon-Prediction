
        data {
        int<lower=1> N;
        vector[N] x;
        vector[N] y;
    }
    parameters {
        real alpha;
        real beta;
        real<lower=0> sigma;
    }
    model {
        y ~ normal(alpha + beta * x, sigma);
        alpha ~ normal(1, 1);
        beta ~ normal(0, 1);
        sigma ~ normal(0, 1);
    }
    generated quantities {
        array[N] real y_rep = normal_rng(alpha + beta * x, sigma);
        array[N] real log_lik;
        for (n in 1:N)
            log_lik[n] = normal_lpdf(y[n] | alpha + beta * x[n], sigma);
    }
