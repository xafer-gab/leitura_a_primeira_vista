🎵 **Sight-Reading (Colab)**

A Google Colab Notebook designed for sight-reading practice, focusing on the generation of random musical sequences and the visualization of music notation using *LilyPond*.
This notebook allows musicians and music students to randomly generate rhythmic–melodic sequences with customized parameters (time signatures, note durations, and pitch sets).
Through LilyPond notation, the content can be exported as PNG and .ly files.

The application has the features:

  1. Support for multiple time signatures (e.g., 2/4, 3/4, 4/4, compound meters).
  2. Configurable note values (minim, crotchet, quaver, semiquaver, dotted notes).
  3. Multiple pitch sets including tonal and atonal options.
  4. Randomized octave placement according to clef.

---

**Usage**

Open the notebook in Google Colab.
Select your parameters:

  1. Clef (Treble, Bass, Alto)
  2. Pitch set (e.g., C major, D major, atonal)
  3. Number of octaves
  4. Durations
  5. Time signature
  6. Number of measures

Run the notebook cell and view or download the generated music.

---

**Requirements**

Google Colab or a local Python environment with LilyPond 2.22.1 installed.
