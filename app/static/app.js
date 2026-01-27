document.addEventListener('DOMContentLoaded', () => {
    fetchLogs();

    // Close modal logic
    const modal = document.getElementById('proposal-modal');
    const closeBtn = document.getElementsByClassName('close-btn')[0];

    closeBtn.onclick = function () {
        modal.style.display = "none";
    }

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});

async function fetchLogs() {
    const listContainer = document.getElementById('log-list');
    const loading = document.getElementById('loading');

    try {
        const response = await fetch('/api/v1/voice_logs/');
        if (!response.ok) throw new Error('Failed to fetch logs');

        const logs = await response.json();

        loading.style.display = 'none';
        listContainer.innerHTML = '';

        if (logs.length === 0) {
            listContainer.innerHTML = '<p>No voice logs found.</p>';
            return;
        }

        logs.forEach(log => {
            const card = document.createElement('div');
            card.className = 'card';

            const date = new Date(log.created_at).toLocaleDateString();

            card.innerHTML = `
                <div class="card-header">
                    <span>${log.elevenlabs_voice_id}</span>
                    <span>${date}</span>
                </div>
                <div class="card-content">
                    "${log.transcript}"
                </div>
                <button class="btn" onclick="generateProposal(${log.id})">
                    Generate Proposal
                </button>
            `;
            listContainer.appendChild(card);
        });

    } catch (error) {
        console.error('Error:', error);
        loading.textContent = 'Error loading logs.';
    }
}

async function generateProposal(validLogId) {
    const modal = document.getElementById('proposal-modal');
    const contentDiv = document.getElementById('proposal-content');
    const downloadBtn = document.getElementById('download-pdf-btn');

    // Show modal loading state
    contentDiv.textContent = 'Generating proposal... please wait...';
    downloadBtn.style.display = 'none'; // Hide until ready
    modal.style.display = "flex";

    try {
        const response = await fetch(`/api/v1/voice_logs/${validLogId}/proposal`);
        if (!response.ok) throw new Error('Failed to generate proposal');

        const data = await response.json();
        contentDiv.textContent = data.proposal;

        // Setup View Web Proposal button
        downloadBtn.innerHTML = '<i class="fas fa-external-link-alt"></i> View Official Proposal';
        downloadBtn.style.display = 'inline-block';
        downloadBtn.onclick = () => {
            window.open(`/api/v1/voice_logs/${validLogId}/proposal/html`, '_blank');
        };

    } catch (error) {
        console.error('Error:', error);
        contentDiv.textContent = 'Error generating proposal.';
        downloadBtn.style.display = 'none';
    }
}
