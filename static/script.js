document.addEventListener('DOMContentLoaded', () => {

    // Helper to handle form submission
    // Helper to handle form submission
    const handleForm = (formId, endpoint) => {
        const form = document.getElementById(formId);
        if (!form) return;

        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            // UI Loading State
            const btn = form.querySelector('button[type="submit"]');
            const originalText = btn.innerHTML;
            btn.innerHTML = 'Processing...';
            btn.disabled = true;

            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await fetch(`/api/predict/${endpoint}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                const resultBox = document.getElementById('result');

                // Reset UI
                if (resultBox) {
                    resultBox.classList.remove('d-none');
                    resultBox.classList.remove('alert-danger', 'alert-success', 'alert-light'); // Clear old
                }

                if (response.ok) {
                    if (endpoint === 'regression') {
                        resultBox.className = 'alert alert-info mt-4 text-center shadow-sm';
                        resultBox.innerHTML = `<h4 class="alert-heading">Predicted MPG</h4><p class="display-4 fw-bold mb-0">${result.mpg}</p>`;
                    }
                    else if (endpoint === 'naive_bayes') {
                        // Assuming result.infected is "Infected" or "Not Infected" or similar
                        const isRisk = result.infected.toLowerCase().includes('infected') || result.infected.toLowerCase().includes('yes');
                        resultBox.className = isRisk ? 'alert alert-danger mt-4 text-center shadow-sm' : 'alert alert-success mt-4 text-center shadow-sm';
                        resultBox.innerHTML = `<h4 class="alert-heading">Risk Assessment</h4><p class="display-6 fw-bold mb-0">${result.infected}</p>`;
                    }
                    else if (endpoint === 'kmeans') {
                        // Special handling for KMeans dashboard card
                        const badge = document.getElementById('clusterBadge');
                        if (badge) {
                            badge.innerText = result.cluster;
                            // Ensure the parent result container is visible
                            resultBox.classList.remove('d-none');
                            // We don't overwrite innerHTML here, just show the container
                        } else {
                            // Fallback
                            resultBox.innerHTML = `Cluster: ${result.cluster}`;
                        }
                    }
                } else {
                    if (resultBox) {
                        resultBox.className = 'alert alert-warning mt-4 text-center';
                        resultBox.innerHTML = `<strong>Error:</strong> ${result.error}`;
                    }
                }
            } catch (err) {
                console.error(err);
                if (document.getElementById('result')) {
                    document.getElementById('result').innerHTML = 'An unexpected error occurred.';
                }
            } finally {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }
        });
    };

    handleForm('regressionForm', 'regression');
    handleForm('naiveBayesForm', 'naive_bayes');
    handleForm('kmeansForm', 'kmeans');
});
