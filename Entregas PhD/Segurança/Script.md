Slide 1:
Good afternoon everyone.
'll present our work on "Machine Unlearning for IoT in Intelligent Buildings." As we integrate AI more deeply into our living spaces, we face a critical challenge: how do we ensure privacy when models refuse to forget?

Slide 2:
Smart buildings are essentially ecosystems of sensors. These devices generate longitudinal footprints of our behavior. While this optimizes comfort and energy, it creates a massive digital footprint. Even if we delete the raw data, the models trained on it retain statistical traces that can be exploited.

Slide 3:
Deleting raw data is no longer enough. Machine learning models "memorize" their training sets. Through Membership Inference and Model Inversion attacks, an adversary can reconstruct private resident information. Machine Unlearning is the technical response to this-it's the process of selectively removing data influence.

Slide 4:
GDPR Article 17, the 'Right to be Forgotten, requires that organizations not only delete raw records but any derived influence. For a building operator, a resident moving out means they must expunge that person's history from the HVAC, security, and energy models to remain compliant.

Slide 5:
Unlike a personal smartphone, building data is 'entangled.' If one tenant in a shared office revokes consent, their data is mixed with their coworkers' on the same environmental sensors. Removing one user's influence without degrading the model's performance for everyone else is a major hurdle.

Slide 6/7:
When we look at current methods, we see clear gaps. Cloud methods like SISA ignore the edge limitations. Edge-side gradient ascent is fast but ignores the multi-tenant hierarchy. Federated unlearning exists but it weakens the 'erasure' guarantee itself, often relying on statistical proof rather than certainty.

Slide 8/9/10:
The 'Gap' is significant. Most unlearning research is developed in silos. We found that only a small fraction of methods consider edge resource limits, and even fewer provide the kind of verification that a regulator would accept as true 'erasure’

Slide 11:
How do we fix this?
First: Scalability. We need ‘TinyML Unlearning’. Instead of full retraining, we use sparse updates and hardware-accelerated paths to perform erasure directly on the edge hardware without overwhelming the system.
Second: Verification. We need more thanjust 'trust me' from a building vendor. We need hardware attestations (TEEs) and Zero-Knowledge Proofs to certify to residents and regulators that their data influence is truly gone.
To conclude, machine unlearning in smart buildings is not just an academic problem-it's a regulatory necessity. We need to move from cloud-centric methods to distributed, verifiable systems. Thank you for your time, and I am now open to any questions.