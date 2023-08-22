
data {
  int<lower=0> N;  // observations
  int<lower=1> J;  // counties
  array[N] int<lower=1, upper=J> county;
  vector[N] x;     // floor
}
generated quantities {
  real mu_alpha = normal_rng(1, 1);
  real<lower=0> sigma_alpha = fabs(normal_rng(0, 1));
  vector[J] alpha;
  
  for (j in 1:J) {
    alpha[j] = normal_rng(mu_alpha, sigma_alpha);
  }
  
  real mu_beta = normal_rng(0, 1);
  real<lower=0> sigma_beta = fabs(normal_rng(0, 1));
  vector[J] beta;
  
  for (j in 1:J) {
    beta[j] = normal_rng(mu_beta, sigma_beta);
  }
  
  real sigma = fabs(normal_rng(0, 1));

  real y_sim[N];
  
  for (i in 1:N) {
    y_sim[i] = normal_rng(alpha[county[i]] + beta[county[i]] * x[i], sigma);
  }
}
