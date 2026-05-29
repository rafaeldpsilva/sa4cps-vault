Slide 1:
Good afternoon everyone.
'll present our work on "Machine Unlearning for IoT in Intelligent Buildings." As we integrate AI more deeply into our living spaces, we face a critical challenge: how do we ensure privacy when models refuse to forget?

Slide 2:
Smart buildings are essentially ecosystems of sensors. These devices generate longitudinal footprints of our behavior. While this optimizes comfort and energy, it creates a massive digital footprint. Even if we delete the raw data, the models trained on it retain statistical traces that can be exploited.

Slide 3:
Deleting raw data is no longer enough. Machine learning models "memorize" their training sets. Through Membership Inference and Model Inversion attacks, an adversary can reconstruct private resident information. Machine Unlearning is the technical response to this-it's the process of selectively removing data influence.

Slide 4:
GDPR Article 17, the 'Right to be Forgotten, requires that organizations not only delete raw records but any derived influence. For a building operator, a resident moving out means they must expunge that person's history from the HVAC, security, and energy models to remain compliant.
