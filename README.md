# Imprint Verify

Web verifier for **Imprint** proofs: **[imprintproof.app](https://imprintproof.app)**

Imprint is an app for the Solana Seeker phone. When you take a photo, the phone's secure chip signs the photo
together with what its sensors read at that instant, and your wallet seals the fingerprint on Solana. This page
lets anyone check such a proof in a browser, without a Seeker and without an account.

## How to check a proof

**You took the photo** (on your Seeker):

1. **Open it in Imprint**: go to Journal and tap the photo.
2. **Save both files**: tap "Save photo + proof to phone". The photo (`.jpg`) and its proof (`.proof.json`)
   land in `Download/Imprint`.
3. **Send both files** together. A proof contains the exact place: share it only with people you trust.

**Someone sent you a proof:**

1. **Keep both files**: save the photo and its `.proof.json` on your phone or computer. One without the other
   can't be checked.
2. **Drop them**: open [imprintproof.app](https://imprintproof.app) and drop both files on the round stamp, or
   tap "Choose files" and select both.
3. **Read the verdict**: "Authentic" in green means all five checks passed. Any other verdict says what is not
   proven.

## The five checks

1. **The photo**: its SHA-256 fingerprint must match the one signed at capture. Change one pixel and it fails.
2. **The readings**: time, GPS, compass, barometer, light, sound, motion and NFC are hashed together with the
   photo. The phone also records whether the GPS position was simulated, and how long before the photo it was
   measured.
3. **The phone signature**: the phone's secure chip signs that hash. The private key never leaves the chip.
4. **The chip itself**: a certificate chain signed by Google proves the key lives in real phone hardware, was
   created by the official Imprint app on an unmodified phone, and was not revoked.
5. **The Solana seal**: the hash is written in a Solana memo. The block time proves the photo existed no later
   than that moment.

## Privacy

Everything is checked in your browser. The files are never uploaded. The only network request asks a Solana node
(Helius, or a public node as a fallback) for the transaction named in the proof. GPS and sensor readings are never
written on-chain, only their hash. The place is shown only if you press "Show the place".

## What a proof does not show

A proof shows what this phone recorded, and when. It does not prove that the scene itself is real, or who was
holding the phone.

## In this repository

- `index.html`: the whole verifier, in one file, with a strict Content Security Policy.
- `fonts/`: self-hosted fonts (Archivo, Archivo Narrow, Courier Prime) and their OFL licences.
- `revocations.json`: Google's list of revoked attestation keys, refreshed every day by a GitHub Action
  (`.github/workflows/`, `update-revocations.py`), so a revoked chip key stops passing within a day.
- `privacy.html`, `terms.html`: privacy policy and terms of use.

Published by SolanaChetis.
