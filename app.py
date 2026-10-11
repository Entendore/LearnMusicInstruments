import sys
import random
import re
import webbrowser
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QListWidget, QLineEdit, QLabel, 
                               QSplitter, QFrame, QComboBox, QPushButton, 
                               QCheckBox, QTabWidget, QGridLayout, QScrollArea,
                               QFileDialog, QMessageBox)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices, QGuiApplication, QShortcut, QKeySequence

# --- Expanded Data (190+ Instruments) ---
INSTRUMENTS_DATA = [
    {"name": "Accordion", "culture": "European", "type": "Wind (Free Reed)", "origin": "Europe", "emoji": "🎹", "description": "A family of box-shaped musical instruments of the bellows-driven free-reed aerophone type. Consists of a bellows and two keyboards.", "playing": "Played by expanding and compressing the bellows while pressing buttons or keys on the right side (melody) and left side (bass/chords).", "learning": "1. Learn the bass buttons (fundamental basses and major chords). 2. Coordinate bellows direction with note changes. 3. Practice right-hand melody independently before combining.", "difficulty": "Intermediate"},
    {"name": "Algaita", "culture": "West Africa", "type": "Wind (Reed)", "origin": "Nigeria", "emoji": "🎺", "description": "A double-reed wind instrument from West Africa, related to the shawm.", "playing": "Blown through a double reed. Fingers cover holes. It produces a loud, piercing sound often used in Hausa ceremonial music.", "learning": "1. Learn to control breath pressure for the double reed. 2. Master the traditional Hausa melodic patterns.", "difficulty": "Advanced"},
    {"name": "Angklung", "culture": "Southeast Asian", "type": "Percussion", "origin": "Indonesia", "emoji": "🎋", "description": "An Indonesian musical instrument made of bamboo tubes suspended in a bamboo frame.", "playing": "Shaken laterally. Each tube plays a single note. Often played in large ensembles where each player shakes a specific note to create melodies.", "learning": "1. Learn the basic shake technique (swift lateral motion). 2. Play in a group to understand interlocking melodies.", "difficulty": "Beginner"},
    {"name": "Anzad", "culture": "North African", "type": "String (Bowed)", "origin": "Sahara (Tuareg)", "emoji": "🎻", "description": "A one-stringed bowed lute played by the Tuareg people of the Sahara.", "playing": "Bowed with a horsehair bow. The single string is made of horsehair.", "learning": "1. Master the bowing rhythm. 2. Coordinate with traditional Tuareg vocal chants.", "difficulty": "Advanced", "classification": "Chordophone", "fact": "The Anzad is a one-stringed Tuareg fiddle traditionally played by women to accompany epic poetry."},
    {"name": "Appalachian Dulcimer", "culture": "North American", "type": "String (Plucked)", "origin": "USA (Appalachia)", "emoji": "🎸", "description": "A fretted string instrument of the zither family, typically with three or four strings.", "playing": "Laid flat on the lap and plucked or strummed with a feather or pick. Noted for its soft, sweet sound.", "learning": "1. Learn the traditional DAD tuning. 2. Master playing melodies on the melody string while drones ring out.", "difficulty": "Beginner", "classification": "Chordophone"},
    {"name": "Asaoto", "culture": "West Africa", "type": "Percussion", "origin": "Ghana", "emoji": "🪵", "description": "A large rooted wood log drum from Ghana, originally used for communication between villages.", "playing": "Played with two wooden sticks. The log is hollowed out and has slits of varying sizes to produce different pitches.", "learning": "1. Learn the specific slit locations for each pitch. 2. Master traditional communication rhythms.", "difficulty": "Intermediate"},
    {"name": "Atenteben", "culture": "West African", "type": "Wind", "origin": "Ghana", "emoji": "🪈", "description": "A bamboo flute from Ghana, traditionally played in the Akan region.", "playing": "Blown into the end. Has six finger holes. Often played in ensembles with drums.", "learning": "1. Learn the basic scale. 2. Master traditional Akan melodies.", "difficulty": "Beginner", "classification": "Aerophone", "fact": "The Atenteben was traditionally used for recreational music but has been adapted into contemporary Ghanaian classical music."},
    {"name": "Bandoneon", "culture": "European", "type": "Wind (Free Reed)", "origin": "Germany/Argentina", "emoji": "🎹", "description": "A type of concertina particularly important in Argentine tango.", "playing": "Played by expanding and compressing the bellows while pressing buttons. Unlike an accordion, each button plays a different note on push vs. pull.", "learning": "1. Memorize the differing push/pull notes. 2. Learn the rhythmic 'arrastre' (dragging) technique used in Tango.", "difficulty": "Advanced"},
    {"name": "Bandura", "culture": "Eastern European", "type": "String (Plucked)", "origin": "Ukraine", "emoji": "🎶", "description": "A Ukrainian plucked string folk instrument, combining elements of a box zither and lute.", "playing": "Plucked with both hands. Traditionally, the left hand plays basses while the right hand plays the melody.", "learning": "1. Learn the tuning of the 50+ strings. 2. Master rapid finger plucking techniques.", "difficulty": "Advanced", "classification": "Chordophone"},
    {"name": "Baglama (Saz)", "culture": "Middle East", "type": "String (Plucked)", "origin": "Turkey", "emoji": "🎸", "description": "The most common Turkish stringed instrument, belonging to the lute family.", "playing": "Plucked with a small plectrum (tezene). Features movable frets tied to the neck, allowing for microtonal scales (makams).", "learning": "1. Learn the standard baglama tuning. 2. Master the downward/upward picking pattern. 3. Learn Turkish makams (scales).", "difficulty": "Intermediate"},
    {"name": "Bagpipes", "culture": "Celtic", "type": "Wind (Reed)", "origin": "Scotland/Europe", "emoji": "🎶", "description": "A wind instrument using enclosed reeds fed from a constant reservoir of air in the form of a bag.", "playing": "The player fills the bag with air via a blowpipe and applies pressure with the arm. Air passes over reeds in the chanter (melody) and drones (harmony).", "learning": "1. Master the practice chanter before touching the pipes. 2. Learn to maintain steady pressure on the bag. 3. Practice scales and grace notes on the chanter.", "difficulty": "Advanced"},
    {"name": "Balalaika", "culture": "Russian", "type": "String (Plucked)", "origin": "Russia", "emoji": "🎸", "description": "A Russian stringed musical instrument with a characteristic triangular wooden, hollow body and three strings.", "playing": "Played with the fingers or a plectrum. The player uses a 'tremolo' technique (rapid up-and-down picking) to sustain notes.", "learning": "1. Learn basic open string plucking. 2. Master the tremolo technique. 3. Learn chord shapes up the neck.", "difficulty": "Intermediate"},
    {"name": "Bansuri", "culture": "India", "type": "Wind", "origin": "India", "emoji": "🪈", "description": "A side-blown flute made of bamboo. It is an ancient instrument associated with cowherds and the Hindu god Krishna.", "playing": "Blown transversely (sideways). Fingers open and close holes. Pitch is bent by partially covering holes and changing blowing angle.", "learning": "1. Learn to produce a clean, steady tone. 2. Master the fingering for a major scale. 3. Learn breath control for long sustains.", "difficulty": "Intermediate"},
    {"name": "Bata", "culture": "Caribbean/Latin", "type": "Percussion", "origin": "Nigeria/Cuba", "emoji": "🥁", "description": "A double-headed drum shaped like an hourglass with one cone larger than the other.", "playing": "Placed on the lap and played with both hands. It is central to Santeria religious music.", "learning": "1. Learn the specific hand strokes for the smaller head (high pitch) and larger head (low pitch). 2. Study the sacred Toques (rhythms) of Santeria.", "difficulty": "Advanced"},
    {"name": "Bawu", "culture": "Chinese", "type": "Wind (Reed)", "origin": "China (Yunnan)", "emoji": "🫛", "description": "A Chinese free-reed wind instrument with a pure, clarinet-like tone.", "playing": "Blown into a mouthpiece containing a brass reed. Fingers cover holes.", "learning": "1. Learn breath control for the free reed. 2. Master traditional Chinese melodies.", "difficulty": "Beginner", "classification": "Aerophone", "fact": "The Bawu produces a remarkably pure, mellow tone that sounds like a clarinet but operates like a harmonica."},
    {"name": "Bendir", "culture": "Middle East", "type": "Percussion", "origin": "North Africa", "emoji": "🥁", "description": "A traditional frame drum used in North Africa and Middle Eastern music.", "playing": "Held in one hand and struck with the fingers of the other. Often features a snare string stretched across the back of the head for a buzzing effect.", "learning": "1. Learn the traditional finger-striking techniques. 2. Master the 'rub' stroke to utilize the snare buzz effectively.", "difficulty": "Intermediate"},
    {"name": "Berimbau", "culture": "South American", "type": "String (Struck)", "origin": "Brazil/Angola", "emoji": "🏹", "description": "A single-string percussion instrument, a musical bow, from Brazil, closely associated with capoeira.", "playing": "The player holds a bow and strikes the wire string with a thin stick (vaqueta). A small gourd (cabaça) resonates the sound, opened/closed against the stomach to change pitch.", "learning": "1. Learn to hold the bow and balance the cabaça. 2. Practice striking the string and pressing the coin to get two distinct pitches. 3. Learn the basic capoeira rhythms.", "difficulty": "Intermediate"},
    {"name": "Biwa", "culture": "Japan", "type": "String (Plucked)", "origin": "Japan/China", "emoji": "🎸", "description": "A Japanese short-necked fretted lute, often used in narrative storytelling.", "playing": "Plucked with a large wooden plectrum called a bachi. The player often strikes the skin of the instrument for percussive effect.", "learning": "1. Learn the specific tuning for your style of Biwa. 2. Master coordinating sung narrative with plectrum strikes.", "difficulty": "Advanced"},
    {"name": "Bodhrán", "culture": "Celtic", "type": "Percussion", "origin": "Ireland", "emoji": "🥁", "description": "An Irish frame drum ranging from 25 to 65 cm in diameter.", "playing": "Played with a wooden tipper (cipín) or bare hands. The left hand presses against the inside of the skin to alter pitch and timbre.", "learning": "1. Hold the tipper correctly. 2. Learn the 'down-up' stroke (jig or reel timing). 3. Practice muting the skin with your inside hand.", "difficulty": "Beginner"},
    {"name": "Bombo", "culture": "Andean", "type": "Percussion", "origin": "Andes", "emoji": "🥁", "description": "A traditional drum of Andean origin, made of a hollow tree trunk with animal skin stretched over the top.", "playing": "Struck with a mallet on one side (deep boom) and a thin stick on the other (high pitch).", "learning": "1. Learn the two-handed stick technique. 2. Master the heartbeat rhythm of Andean music (huayno).", "difficulty": "Beginner"},
    {"name": "Bonang", "culture": "Southeast Asian", "type": "Percussion", "origin": "Indonesia", "emoji": "🛎️", "description": "A musical instrument used in the Javanese gamelan. A collection of small gongs placed horizontally.", "playing": "Struck with two padded mallets. Often plays intricate, interlocking melodic patterns (kotekan).", "learning": "1. Listen to gamelan music to understand cyclical melodies. 2. Practice striking the center boss (penyu) cleanly.", "difficulty": "Intermediate"},
    {"name": "Bouzouki", "culture": "European", "type": "String (Plucked)", "origin": "Greece", "emoji": "🎸", "description": "A Greek stringed instrument with a pear-shaped body and a long neck, central to Rebetiko music.", "playing": "Plucked with a plectrum. Often features rapid tremolo playing and chordal backing.", "learning": "1. Learn the standard Greek tuning (ADAD or CFAD). 2. Master the tremolo picking technique. 3. Learn Rebetiko scales (Dromoi).", "difficulty": "Intermediate"},
    {"name": "Buk", "culture": "Korean", "type": "Percussion", "origin": "Korea", "emoji": "🥁", "description": "A traditional Korean shallow barrel drum.", "playing": "Played with a single wooden stick on a wooden frame. Produces a deep, resonant thud.", "learning": "1. Learn the basic stick strike. 2. Coordinate with traditional Korean rhythms (Jangdan).", "difficulty": "Beginner", "classification": "Membranophone", "fact": "The Buk is a staple of Korean traditional music (Gugak) and is often played alongside the hourglass-shaped Janggu drum."},
    {"name": "Cajón", "culture": "South American", "type": "Percussion", "origin": "Peru", "emoji": "📦", "description": "A box-shaped percussion instrument originally from Peru, played by slapping the front face.", "playing": "The player sits on the box and slaps the front face. The top edge gives a high crack, the center gives a deep bass tone.", "learning": "1. Master the bass stroke vs. the slap stroke. 2. Learn basic Afro-Peruvian or Flamenco rhythms.", "difficulty": "Beginner"},
    {"name": "Cavaquinho", "culture": "Caribbean/Latin", "type": "String (Plucked)", "origin": "Portugal/Brazil", "emoji": "🎸", "description": "A small Portuguese string instrument, similar to a ukulele, central to Brazilian Samba and Choro.", "playing": "Strummed with a pick. Provides the rhythmic 'swing' in samba bands.", "learning": "1. Learn standard open chord shapes. 2. Master the rapid samba strumming pattern.", "difficulty": "Beginner", "classification": "Chordophone"},
    {"name": "Chapman Stick", "culture": "North American", "type": "String (Tapped)", "origin": "USA", "emoji": "🎸", "description": "A wide fretboard with 10 or 12 strings, played exclusively by two-handed tapping.", "playing": "Both hands tap the strings directly against the frets to sound notes, allowing the player to play bass and melody simultaneously.", "learning": "1. Learn independent left/right hand tapping. 2. Coordinate bass and melody lines.", "difficulty": "Advanced", "classification": "Chordophone", "fact": "Invented by Emmett Chapman in the early 1970s, the Chapman Stick allows a single player to perform bass, chords, and melody simultaneously."},
    {"name": "Charango", "culture": "Andean", "type": "String (Plucked)", "origin": "Andes Mountains", "emoji": "🎸", "description": "A small Andean stringed instrument of the lute family, traditionally made with an armadillo shell.", "playing": "Plucked or strummed with the fingers. Often uses rapid rasgueado (strumming) patterns.", "learning": "1. Learn the 10-string tuning (pairs). 2. Practice basic strumming patterns. 3. Learn traditional Andean melodies.", "difficulty": "Intermediate"},
    {"name": "Cimbalom", "culture": "European", "type": "String (Struck)", "origin": "Hungary", "emoji": "🔨", "description": "A large concert hammered dulcimer played primarily in Central and Eastern Europe.", "playing": "Struck with two curved wooden mallets wrapped in cotton. Features a massive range of strings and a damper pedal.", "learning": "1. Learn to strike cleanly without hitting adjacent notes. 2. Master crossing hands. 3. Use the damper pedal effectively.", "difficulty": "Advanced"},
    {"name": "Cimpoi", "culture": "Balkan", "type": "Wind (Reed)", "origin": "Romania", "emoji": "🎶", "description": "A traditional Romanian bagpipe.", "playing": "Air is blown into the bag, which feeds a chanter with a double reed and a bass drone.", "learning": "1. Master maintaining pressure on the bag. 2. Learn traditional Romanian dance tunes.", "difficulty": "Advanced", "classification": "Aerophone", "fact": "The Cimpoi is a traditional Romanian bagpipe, often played at weddings and village festivals alongside the fluer (flute)."},
    {"name": "Clapsticks", "culture": "Aboriginal Australian", "type": "Percussion", "origin": "Australia", "emoji": "🥢", "description": "A type of drumstick used to maintain rhythm in Aboriginal Australian music.", "playing": "Struck together to provide a steady rhythm to accompany the didgeridoo.", "learning": "1. Practice holding them loosely for a resonant click. 2. Match the rhythm to natural walks or heartbeats.", "difficulty": "Beginner"},
    {"name": "Conga", "culture": "Caribbean/Latin", "type": "Percussion", "origin": "Cuba/Africa", "emoji": "🥁", "description": "A tall, narrow, single-headed drum from Cuba, derived from African drums.", "playing": "Played with the hands. Five basic strokes: Open Tone, Muffled Tone, Bass Tone, Slap, and Touch.", "learning": "1. Master the 5 basic hand strokes. 2. Learn the fundamental Cuban rhythm (Tumbao).", "difficulty": "Intermediate"},
    {"name": "Crumhorn", "culture": "European", "type": "Wind (Reed)", "origin": "Europe", "emoji": "🎵", "description": "A musical instrument of the woodwind family, most commonly used during the Renaissance period.", "playing": "Blown through a double reed enclosed in a windcap. Features a curved, J-shaped body.", "learning": "1. Learn to maintain steady breath pressure. 2. Master Renaissance fingerings.", "difficulty": "Intermediate"},
    {"name": "Crwth", "culture": "Celtic", "type": "String (Bowed)", "origin": "Wales", "emoji": "🎻", "description": "An ancient Celtic bowed lyre from Wales.", "playing": "Bowed with the right hand while the left hand stops the strings on a fingerboard. It has a distinct flat bridge and plays drone notes.", "learning": "1. Learn the unique flat-bridge tuning. 2. Master playing drone and melody strings simultaneously.", "difficulty": "Advanced"},
    {"name": "Cuatro", "culture": "Caribbean/Latin", "type": "String (Plucked)", "origin": "Venezuela", "emoji": "🎸", "description": "A small Latin American string instrument of the guitar family, typically with four strings.", "playing": "Plucked or strummed with a pick. The Venezuelan cuatro is the national instrument and features a unique 'stride' strumming pattern.", "learning": "1. Learn the ADGB standard tuning. 2. Master the intricate strumming patterns (temple).", "difficulty": "Intermediate", "classification": "Chordophone", "fact": "The Cuatro is the national instrument of Venezuela, traditionally featuring 4 strings but sometimes having 14 strings grouped in 4 courses."},
    {"name": "Cuíca", "culture": "South American", "type": "Percussion", "origin": "Brazil", "emoji": "🪣", "description": "A Brazilian friction drum often used in samba music, known for its high, squeaky, monkey-like sound.", "playing": "A bamboo stick is attached to the drumhead inside. The player rubs the stick with a wet cloth to create friction, changing pitch by pressing the skin.", "learning": "1. Perfect the rubbing technique to get a steady squeak. 2. Practice altering pitch with your thumb on the drumhead.", "difficulty": "Intermediate"},
    {"name": "Daf", "culture": "Middle East", "type": "Percussion", "origin": "Persia/Kurdistan", "emoji": "🥁", "description": "A large Persian frame drum used in Kurdish and Middle Eastern music.", "playing": "Played with the hands. Features heavy metal rings attached to the inside of the frame, which jingle when struck.", "learning": "1. Learn the 'Tom' (bass) and 'Bak' (snap) strokes. 2. Master the roll technique using the fingers.", "difficulty": "Intermediate", "classification": "Membranophone", "fact": "The Daf is heavily associated with Sufi mystical music and features internal metal rings that create a continuous jingle."},
    {"name": "Dan Bau", "culture": "Southeast Asian", "type": "String (Plucked)", "origin": "Vietnam", "emoji": "🎶", "description": "A Vietnamese monochord (one-string) zither.", "playing": "Plucked with a plectrum. Pitch is bent by pushing/pulling a flexible bamboo stem attached to the string, creating its signature wailing sound.", "learning": "1. Pluck the open string. 2. Master the microtonal bending with the bamboo stem. 3. Learn traditional Vietnamese scales.", "difficulty": "Intermediate"},
    {"name": "Dan Moi", "culture": "Southeast Asian", "type": "Percussion (Lamellophone)", "origin": "Vietnam", "emoji": "👅", "description": "A Vietnamese jaw harp made of brass.", "playing": "Placed against the lips and plucked. The mouth cavity acts as a resonator, and the player changes pitch and timbre by altering mouth shapes.", "learning": "1. Learn to pluck rhythmically without hurting teeth. 2. Master changing mouth shapes to create melodic overtones.", "difficulty": "Beginner"},
    {"name": "Dan Nguyet", "culture": "Southeast Asian", "type": "String (Plucked)", "origin": "Vietnam", "emoji": "🎸", "description": "A Vietnamese two-stringed lute with a flat circular body.", "playing": "Plucked with a plectrum or fingers. The neck is fretless. Often plays bright, lyrical melodies.", "learning": "1. Learn the traditional tuning. 2. Master the vibrato techniques.", "difficulty": "Intermediate", "classification": "Chordophone", "fact": "Also known as the 'Moon Lute' due to its circular soundbox, the Dan Nguyet is heavily used in traditional Vietnamese court music."},
    {"name": "Daegeum", "culture": "Korean", "type": "Wind", "origin": "Korea", "emoji": "🪈", "description": "A large transverse bamboo flute used in traditional Korean music.", "playing": "Blown transversely. Has a buzzing membrane (cheong) between the mouthpiece and finger holes, giving it a distinct reedy timbre.", "learning": "1. Learn breath control. 2. Master traditional Korean scales and ornaments.", "difficulty": "Advanced", "classification": "Aerophone", "fact": "The Daegeum has a buzzing membrane similar to the Chinese Dizi, giving it a distinct reedy timbre used in court and folk music."},
    {"name": "Darbuka", "culture": "Middle East", "type": "Percussion", "origin": "Middle East", "emoji": "🥁", "description": "A single-head membranophone with a goblet-shaped body.", "playing": "Played with the hands. 'Dum' is a deep bass stroke in the center; 'Tak' is a sharp higher stroke on the edge.", "learning": "1. Master the Dum (center) and Tak (edge) strokes. 2. Learn basic Middle Eastern rhythms like Maqsoum and Baladi.", "difficulty": "Beginner"},
    {"name": "Didgeridoo", "culture": "Aboriginal Australian", "type": "Wind", "origin": "Northern Australia", "emoji": "喇叭", "description": "A wind instrument developed by Aboriginal peoples of northern Australia.", "playing": "Played with vibrating lips (similar to a brass instrument). Requires 'circular breathing' to play continuously.", "learning": "1. Learn circular breathing (practice blowing water through a straw). 2. Master vocalizations and animal sounds on top of the drone.", "difficulty": "Intermediate"},
    {"name": "Dilli Kaval", "culture": "Middle East", "type": "Wind", "origin": "Kurdistan", "emoji": "🪈", "description": "A traditional Kurdish block flute, similar to a recorder but with 7 holes.", "playing": "Blown into a fipple mouthpiece. Fingers cover holes. Often plays haunting, emotional melodies.", "learning": "1. Learn the basic scale. 2. Master breath control for dynamic contrast.", "difficulty": "Beginner", "classification": "Aerophone"},
    {"name": "Dilruba", "culture": "India", "type": "String (Bowed)", "origin": "India", "emoji": "🎻", "description": "A stringed instrument used in Sikh music and Hindustani classical music.", "playing": "Bowed with the right hand. The left hand moves over the frets, but the strings are pressed *underneath* the frets (like a sitar) to bend pitch.", "learning": "1. Learn to press the strings under the frets. 2. Coordinate bowing with left-hand slides (meend).", "difficulty": "Advanced"},
    {"name": "Dizi", "culture": "China", "type": "Wind", "origin": "China", "emoji": "🪈", "description": "A Chinese transverse flute.", "playing": "Blown transversely. Has an extra hole covered by a thin membrane (dimo) which gives it a buzzing, resonant quality.", "learning": "1. Apply the dimo membrane correctly. 2. Learn standard fingerings. 3. Practice Chinese trills and grace notes.", "difficulty": "Intermediate"},
    {"name": "Djembe", "culture": "West Africa", "type": "Percussion", "origin": "Mali Empire", "emoji": "🥁", "description": "A rope-tuned skin-covered goblet drum played with bare hands.", "playing": "Played with bare hands. Three main sounds: Bass (center), Tone (edge with firm hand), Slap (edge with loose fingers).", "learning": "1. Perfect hand posture for Tone and Slap. 2. Learn standard West African polyrhythms.", "difficulty": "Beginner"},
    {"name": "Dombra", "culture": "Central Asian", "type": "String (Plucked)", "origin": "Kazakhstan", "emoji": "🎸", "description": "A long-necked lute from Kazakhstan.", "playing": "Plucked or strummed with the fingers. Often used to accompany traditional storytelling (Kuī).", "learning": "1. Learn to strum rapid patterns (tremolo). 2. Memorize basic two-string melodies.", "difficulty": "Beginner"},
    {"name": "Doshpuluur", "culture": "Central Asian", "type": "String (Plucked)", "origin": "Tuva", "emoji": "🎸", "description": "A Tuvan long-necked lute.", "playing": "Plucked or strummed. The neck is fretless, allowing for sliding notes.", "learning": "1. Learn basic open tunings. 2. Coordinate with Tuvan throat singing.", "difficulty": "Beginner", "classification": "Chordophone", "fact": "The Doshpuluur is often used to accompany Tuvan throat singing, featuring a trapezoidal body and a long, fretless neck."},
    {"name": "Doyra", "culture": "Central Asian", "type": "Percussion", "origin": "Uzbekistan", "emoji": "🥁", "description": "A Central Asian frame drum with jingles inside the rim.", "playing": "Played with the fingers. The player strikes the center for a bass tone and the edge for a sharp, jingling tone.", "learning": "1. Learn the basic finger strikes. 2. Master the roll technique using the rim jingles.", "difficulty": "Intermediate", "classification": "Membranophone", "fact": "The Doyra is a frame drum similar to a tambourine but is played with the hands to create complex, syncopated rhythms."},
    {"name": "Dramyin", "culture": "Himalayan", "type": "String (Plucked)", "origin": "Tibet", "emoji": "🎸", "description": "A traditional Tibetan lute with six strings.", "playing": "Plucked with a plectrum. Features a long fretless neck, allowing for sliding notes.", "learning": "1. Practice sliding between notes on the fretless neck. 2. Learn Tibetan folk song melodies.", "difficulty": "Intermediate"},
    {"name": "Duduk", "culture": "Middle East", "type": "Wind (Reed)", "origin": "Armenia", "emoji": "🪈", "description": "An ancient double-reed woodwind instrument native to Armenia.", "playing": "Blown through a large, flat double reed. Fingers cover holes. Produces a warm, mournful, and highly expressive tone.", "learning": "1. Master breath control and circular breathing for the stiff reed. 2. Learn the Armenian modal system (Saz).", "difficulty": "Advanced"},
    {"name": "Dutar", "culture": "Central Asian", "type": "String (Plucked)", "origin": "Uzbekistan/Iran", "emoji": "🎸", "description": "A Central Asian long-necked lute with two strings.", "playing": "Plucked with the fingers. The strings were traditionally made of silk.", "learning": "1. Learn the standard tuning. 2. Master the tremolo strumming technique.", "difficulty": "Intermediate", "classification": "Chordophone", "fact": "The name 'Dutar' translates directly to 'two strings' in Persian."},
    {"name": "Erhu", "culture": "China", "type": "String (Bowed)", "origin": "China", "emoji": "🎻", "description": "A two-stringed bowed musical instrument, sometimes known as the Chinese violin.", "playing": "Bowed with a horsehair bow placed between the two strings. No fingerboard; fingers press strings directly against the snake-skin neck.", "learning": "1. Learn bowing technique (the bow is permanently attached). 2. Master finger pressure without a fretboard. 3. Learn traditional Chinese slides.", "difficulty": "Intermediate"},
    {"name": "Flogera", "culture": "Balkan", "type": "Wind", "origin": "Greece", "emoji": "🪈", "description": "A traditional Greek shepherd's flute.", "playing": "Blown into the end. Has no fipple, requiring the player to shape their lips to direct air.", "learning": "1. Learn the embouchure. 2. Master traditional Greek shepherd melodies.", "difficulty": "Intermediate", "classification": "Aerophone", "fact": "The Flogera is a simple end-blown flute historically played by Greek shepherds to pass the time in the mountains."},
    {"name": "Fujara", "culture": "European", "type": "Wind", "origin": "Slovakia", "emoji": "🪈", "description": "A large, intricately carved overtone flute from Slovakia.", "playing": "Played standing up. Blown into a fipple. Uses a 3-hole fingering system to play natural overtones.", "learning": "1. Learn overtone blowing techniques. 2. Master the 3-hole fingerings to hit specific pitches.", "difficulty": "Intermediate", "classification": "Aerophone"},
    {"name": "Gadulka", "culture": "Balkan", "type": "String (Bowed)", "origin": "Bulgaria", "emoji": "🎻", "description": "A traditional Bulgarian bowed string instrument.", "playing": "Bowed with a horsehair bow. Has 4 playing strings and many sympathetic strings underneath. The player presses the strings with their fingernails, not fingertips.", "learning": "1. Master the painful fingernail technique. 2. Learn asymmetrical Bulgarian dance rhythms.", "difficulty": "Advanced", "classification": "Chordophone", "fact": "Gadulka players press the strings directly with their fingernails rather than the pads of their fingers, allowing for a very specific microtonal style."},
    {"name": "Gaita", "culture": "European", "type": "Wind (Reed)", "origin": "Spain (Galicia)", "emoji": "🎶", "description": "A traditional Galician bagpipe.", "playing": "Air is blown into the bag, feeding a chanter and a bass drone. It is a symbol of Galician culture.", "learning": "1. Master maintaining pressure on the bag. 2. Learn traditional Muiñeira rhythms.", "difficulty": "Advanced", "classification": "Aerophone", "fact": "The Gaita Galega is the symbol of Galician culture in northern Spain and is often played alongside castanets."},
    {"name": "Gankoqui", "culture": "West African", "type": "Percussion (Bell)", "origin": "Ghana/Benin", "emoji": "🔔", "description": "A West African iron bell, also known as an Agogo or Gonkoqui.", "playing": "Struck with a wooden stick. Often plays the timeline pattern in Ewe and Yoruba drum ensembles.", "learning": "1. Learn the basic timeline pattern. 2. Lock into the master drum rhythm.", "difficulty": "Beginner", "classification": "Idiophone", "fact": "The Gankoqui is considered the 'mother instrument' in many West African ensembles, keeping the timeline for all other drums."},
    {"name": "Ghattam", "culture": "India", "type": "Percussion", "origin": "India", "emoji": "🏺", "description": "A percussion instrument used in the Carnatic music of South India. It is a clay pot with a narrow mouth.", "playing": "Played with the hands. The mouth is pressed against the player's stomach to change pitch.", "learning": "1. Learn the basic hand strokes. 2. Master using the stomach to bend the pitch of the pot.", "difficulty": "Intermediate"},
    {"name": "Ghaychak", "culture": "Central Asian", "type": "String (Bowed)", "origin": "Persia/Afghanistan", "emoji": "🎻", "description": "A bowed string instrument used in Iran and Central Asia, featuring a rounded body.", "playing": "Bowed with a horsehair bow. It has four strings and a sympathetic set of strings underneath.", "learning": "1. Learn the bowing pressure. 2. Master traditional Persian scales.", "difficulty": "Advanced", "classification": "Chordophone", "fact": "The Ghaychak has a distinctive spherical body carved from a single piece of mulberry wood."},
    {"name": "Gopichand", "culture": "India", "type": "String (Plucked)", "origin": "India (Bengal)", "emoji": "🎶", "description": "A rhythmic one-string instrument used in Bengali folk music.", "playing": "Plucked with one hand while the other hand squeezes the bamboo sides together to change the tension and pitch of the string.", "learning": "1. Master the squeezing technique to create the characteristic 'bending' sound. 2. Coordinate with traditional Kirtan singing.", "difficulty": "Intermediate", "classification": "Chordophone", "fact": "The Gopichand is heavily associated with Bengali Baul mystics and produces a highly distinctive, bending rhythmic sound."},
    {"name": "Gralla", "culture": "European", "type": "Wind (Reed)", "origin": "Catalonia (Spain)", "emoji": "🎺", "description": "A traditional Catalan double-reed instrument.", "playing": "Blown through a double reed. Fingers cover holes. Produces a loud, strident sound used for outdoor festivals.", "learning": "1. Build embouchure for the hard double reed. 2. Learn traditional Catalan dance melodies.", "difficulty": "Intermediate"},
    {"name": "Gudok", "culture": "Russian", "type": "String (Bowed)", "origin": "Russia", "emoji": "🎻", "description": "An ancient Eastern Slavic string instrument, a bowed harp.", "playing": "Bowed with a horsehair bow. Has 3 strings, all tuned to the same pitch, acting as a drone instrument.", "learning": "1. Learn the constant bowing technique. 2. Master traditional Russian folk melodies.", "difficulty": "Intermediate"},
    {"name": "Guqin", "culture": "China", "type": "String (Plucked)", "origin": "China", "emoji": "🎶", "description": "A plucked seven-string Chinese musical instrument of the zither family.", "playing": "Plucked with the fingers. The left hand presses strings to create vibrato and pitch bends, while the right hand plucks.", "learning": "1. Learn basic right-hand plucking. 2. Master left-hand pitch manipulation. 3. Learn classical ancient notation.", "difficulty": "Advanced", "classification": "Chordophone", "fact": "The Guqin has been played since ancient times and is associated with Chinese scholars and sages for over 3,000 years."},
    {"name": "Gusle", "culture": "Balkan", "type": "String (Bowed)", "origin": "Serbia/Balkans", "emoji": "🎻", "description": "A single-stringed musical instrument traditionally used in the Balkans by epic poets.", "playing": "Bowed continuously while the player sings epic poetry. The string is pressed against the neck by the fingertips or nails.", "learning": "1. Master continuous bowing. 2. Learn to match the drone to vocal recitations.", "difficulty": "Advanced"},
    {"name": "Gusli", "culture": "Russian", "type": "String (Plucked)", "origin": "Russia", "emoji": "🎶", "description": "A traditional Russian plucked string instrument, related to the autoharp.", "playing": "Plucked with the fingers. The player dampens strings they don't want to sound with their left hand while plucking with the right.", "learning": "1. Learn the layout of the diatonic strings. 2. Practice dampening unwanted strings.", "difficulty": "Beginner"},
    {"name": "Guzheng", "culture": "China", "type": "String (Plucked)", "origin": "China", "emoji": "🎶", "description": "A Chinese plucked zither with 16 or more strings and movable bridges.", "playing": "Plucked with artificial fingernails. Pitch is bent by pressing the string on the left side of the bridge.", "learning": "1. Learn right-hand plucking. 2. Master left-hand pitch bending. 3. Combine both for classical pieces.", "difficulty": "Intermediate"},
    {"name": "Handpan", "culture": "European/Modern", "type": "Percussion", "origin": "Switzerland", "emoji": "🛸", "description": "A modern acoustic instrument invented in the year 2000 in Switzerland, known for its ethereal, resonant tones.", "playing": "Played with the hands, usually resting on the player's lap. The player strikes the central note (ding) and the tone fields around it to create melodies and rhythms.", "learning": "1. Learn to strike the tone fields with the soft part of your fingers. 2. Master the 'ding' (center note) rhythm. 3. Explore polyrhythmic patterns.", "difficulty": "Beginner", "classification": "Idiophone", "fact": "The Handpan was invented in the year 2000 in Bern, Switzerland, making it one of the youngest acoustic instruments in the world."},
    {"name": "Hardanger Fiddle", "culture": "Scandinavian", "type": "String (Bowed)", "origin": "Norway", "emoji": "🎻", "description": "The national instrument of Norway, featuring sympathetic strings under the fingerboard.", "playing": "Bowed like a standard violin, but has 4-5 sympathetic strings that resonate underneath.", "learning": "1. Tune the sympathetic strings accurately. 2. Learn traditional Norwegian dance tunes (Springar, Gangar).", "difficulty": "Advanced"},
    {"name": "Harp (Celtic)", "culture": "Celtic", "type": "String (Plucked)", "origin": "Ireland/Scotland", "emoji": "🎶", "description": "A traditional harp with a curved neck and pillar, played on the knee or floor.", "playing": "Plucked with the fingertips. The left hand plays the treble (melody) and the right hand plays the bass (chords).", "learning": "1. Learn proper hand posture. 2. Master playing basic arpeggios and damping strings.", "difficulty": "Intermediate", "classification": "Chordophone"},
    {"name": "Hulusi", "culture": "China", "type": "Wind (Reed)", "origin": "China", "emoji": "🫛", "description": "A free-reed wind instrument from the Dai minority in Yunnan, China. Made of a gourd and bamboo pipes.", "playing": "Blown into the gourd. Has a main melody pipe and one or two drone pipes.", "learning": "1. Learn to maintain a steady breath. 2. Master the fingering on the melody pipe while the drones sound continuously.", "difficulty": "Beginner"},
    {"name": "Hurdy Gurdy", "culture": "European", "type": "String (Bowed)", "origin": "Europe/Middle East", "emoji": "🎹", "description": "A string instrument played by a hand-crank-turned, rosinated wheel rubbing against the strings.", "playing": "The right hand turns the crank. The left hand presses keys to change pitch. A 'buzzing bridge' (chien) creates rhythmic drone effects.", "learning": "1. Master the 'coup' (accelerating the crank to make the buzzing bridge snap). 2. Learn key fingering.", "difficulty": "Advanced"},
    {"name": "Igil", "culture": "Central Asian", "type": "String (Bowed)", "origin": "Tuva", "emoji": "🐎", "description": "A two-stringed Tuvan bowed instrument.", "playing": "Bowed with a horsehair bow. The strings are made of horsehair. Often played with the 4th finger muting strings to create harmonics.", "learning": "1. Learn to rosin and tighten the traditional horsehair bow. 2. Master the traditional overtone techniques.", "difficulty": "Intermediate", "classification": "Chordophone", "fact": "The Igil is heavily associated with Tuvan throat singing and is often carved with a horse's head on the scroll."},
    {"name": "Ipu", "culture": "Polynesian", "type": "Percussion", "origin": "Hawaii", "emoji": "🥥", "description": "A percussion instrument made from gourds, often used by hula dancers.", "playing": "Struck with the hands or on a padded mat. The player holds the gourd and slaps the side and bottom.", "learning": "1. Learn the two distinct tones (center and edge). 2. Coordinate beats with traditional Hula chants (Mele).", "difficulty": "Beginner"},
    {"name": "Janggu", "culture": "Korean", "type": "Percussion", "origin": "Korea", "emoji": "🥁", "description": "A traditional Korean hourglass-shaped drum.", "playing": "Played with two different sticks. Left hand uses a palm stick for deep sounds; right hand uses a bamboo stick for sharp sounds.", "learning": "1. Master the two-stick coordination. 2. Learn traditional Korean rhythms (Jangdan).", "difficulty": "Intermediate"},
    {"name": "Kalimba", "culture": "Southern African", "type": "Percussion (Lamellophone)", "origin": "Africa", "emoji": "🎵", "description": "A modernized version of the mbira, a lamellophone instrument.", "playing": "Plucked with the thumbs. Tines are arranged in a lateral layout (longer in the center, shorter on the edges).", "learning": "1. Learn basic melodies using the center tines. 2. Practice playing glissandos by dragging the thumb across the tines.", "difficulty": "Beginner"},
    {"name": "Kamancha", "culture": "Middle East", "type": "String (Bowed)", "origin": "Persia/Azerbaijan", "emoji": "🎻", "description": "A bowed string instrument played in Azerbaijani, Armenian, and Persian music.", "playing": "Bowed while held vertically. It has a spherical body and four strings.", "learning": "1. Master the vertical bowing posture. 2. Learn the Mugham (modal) system.", "difficulty": "Advanced", "classification": "Chordophone", "fact": "The Kamancha is a core instrument in the Mugham classical music tradition of Azerbaijan."},
    {"name": "Kantele", "culture": "Scandinavian", "type": "String (Plucked)", "origin": "Finland", "emoji": "🎶", "description": "A traditional Finnish and Karelian plucked string instrument (zither).", "playing": "Plucked with the fingers. Traditionally has 5 strings, but modern versions have up to 40.", "learning": "1. Learn the traditional 5-string tuning. 2. Master playing the melody against a drone string.", "difficulty": "Beginner"},
    {"name": "Kaval", "culture": "Balkan", "type": "Wind", "origin": "Balkans/Middle East", "emoji": "🪈", "description": "a chromatic end-blown flute traditionally played throughout the Balkans and Anatolia.", "playing": "Blown across the sharp edge of the open end. Requires a specific 'lip lock'. Often played with a continuous drone note.", "learning": "1. Learn to produce a clear tone. 2. Master breath control. 3. Learn asymmetric Balkan rhythms.", "difficulty": "Intermediate"},
    {"name": "Kazoo", "culture": "North American", "type": "Wind", "origin": "USA", "emoji": "🎺", "description": "A small, simple musical instrument that adds a 'buzzing' timbral quality to the human voice.", "playing": "Hummed into, not blown. The player's voice vibrates a membrane inside the kazoo.", "learning": "1. Practice humming tunes instead of blowing. 2. Master contrasting syllables to change the buzz quality.", "difficulty": "Beginner", "classification": "Aerophone"},
    {"name": "Khene", "culture": "Southeast Asian", "type": "Wind", "origin": "Laos/Thailand", "emoji": "🎵", "description": "A mouth organ of Lao origin made of bamboo pipes connected to a hardwood reservoir.", "playing": "Blown into (exhaled) and drawn out (inhaled) through the mouthpiece. Fingers cover holes on the pipes to isolate notes.", "learning": "1. Practice continuous breathing (circular breathing). 2. Learn the fingering combinations for chords.", "difficulty": "Intermediate"},
    {"name": "Kemenche", "culture": "Middle East", "type": "String (Bowed)", "origin": "Turkey/Persia", "emoji": "🎻", "description": "A bottle-shaped bowed lute used in folk and classical music of the Middle East.", "playing": "Bowed while resting on the knee. Has 3-4 strings. Often plays microtonal melodies.", "learning": "1. Learn the traditional bowing style. 2. Master the microtonal fingerings for Turkish/Persian music.", "difficulty": "Advanced"},
    {"name": "Khlui", "culture": "Southeast Asian", "type": "Wind", "origin": "Thailand", "emoji": "🪈", "description": "A traditional Thai vertical bamboo flute.", "playing": "Blown into a semi-circular mouthpiece. Has 7 finger holes. Produces a clear, sweet tone.", "learning": "1. Learn breath control for dynamic range. 2. Master traditional Thai pentatonic scales.", "difficulty": "Intermediate", "classification": "Aerophone", "fact": "The Khlui is a cornerstone of Thai classical music (Piphat) and comes in various sizes, from soprano to bass."},
    {"name": "Kora", "culture": "West Africa", "type": "String (Plucked)", "origin": "Mandinka Empire", "emoji": "🎵", "description": "A 21-string lute-bridge-harp used extensively in West Africa by griots.", "playing": "Plucked with the thumb and index finger of both hands. The remaining fingers hold the handholds on the neck.", "learning": "1. Learn the bass line (thumb) and melody (index finger) separately. 2. Combine them to create polyphonic music.", "difficulty": "Intermediate"},
    {"name": "Koto", "culture": "Japan", "type": "String (Plucked)", "origin": "Japan/China", "emoji": "🎶", "description": "The national instrument of Japan, a 13-string plucked zither.", "playing": "Plucked with three finger picks (tsume) on the thumb, index, and middle fingers. Bridges can be moved to tune the strings.", "learning": "1. Learn to wear and use the tsume properly. 2. Master standard Japanese pentatonic scales. 3. Practice classical pieces like 'Sakura'.", "difficulty": "Intermediate"},
    {"name": "Kouxian", "culture": "China", "type": "Percussion (Lamellophone)", "origin": "China", "emoji": "👅", "description": "A traditional Chinese jaw harp.", "playing": "Placed against the teeth and plucked. The mouth cavity acts as a resonator, and the player changes pitch and timbre by altering mouth shapes.", "learning": "1. Learn to pluck rhythmically without hurting teeth. 2. Master changing mouth shapes to create melodic overtones.", "difficulty": "Beginner", "classification": "Idiophone", "fact": "Kouxian is often made of bamboo or iron and was historically used by ethnic minorities in China to court lovers."},
    {"name": "Kpanlogo", "culture": "West Africa", "type": "Percussion", "origin": "Ghana", "emoji": "🥁", "description": "A traditional Ghanaian conga-like drum, used in Kpanlogo music.", "playing": "Played with hands. Has a sharp slap and deep tone.", "learning": "1. Learn the hand positions for tone and slap. 2. Master the Kpanlogo dance rhythm.", "difficulty": "Beginner", "classification": "Membranophone"},
    {"name": "Krar", "culture": "East African", "type": "String (Plucked)", "origin": "Ethiopia", "emoji": "🎸", "description": "A five- or six-stringed bowl lyre from Ethiopia, used to accompany singing or as a solo instrument.", "playing": "Plucked or strummed with a plectrum. Often plays a rhythmic ostinato (repeating pattern) to accompany a vocalist.", "learning": "1. Learn the traditional pentatonic tuning. 2. Master the rhythmic strumming style.", "difficulty": "Beginner"},
    {"name": "Launeddas", "culture": "European", "type": "Wind (Reed)", "origin": "Sardinia (Italy)", "emoji": "🫛", "description": "A triple clarinet consisting of three pipes, played with circular breathing.", "playing": "Two pipes play a continuous drone, and the third plays the melody. Requires circular breathing to keep the drones going constantly.", "learning": "1. Master circular breathing. 2. Coordinate finger movements on the melody pipe while holding the heavy drones.", "difficulty": "Advanced", "classification": "Aerophone", "fact": "The Launeddas is an ancient Sardinian instrument that has been played for at least 2,800 years, making it one of the oldest polyphonic instruments in the Mediterranean."},
    {"name": "Lur", "culture": "Scandinavian", "type": "Wind (Reed-less)", "origin": "Scandinavia", "emoji": "📯", "description": "An ancient Scandinavian wind instrument, made of bronze, dating back to the Bronze Age.", "playing": "Blown like a modern brass instrument. Has no finger holes, only playing natural overtones.", "learning": "1. Learn the brass-style embouchure. 2. Master breath control to hit specific overtones.", "difficulty": "Advanced", "classification": "Aerophone"},
    {"name": "Maracas", "culture": "Caribbean/Latin", "type": "Percussion", "origin": "Latin America", "emoji": "🪇", "description": "A rattle which appears in many genres of Caribbean and Latin music.", "playing": "Shaken in pairs. A sharp 'swing' motion sends the beads striking the shell.", "learning": "1. Practice the 'bounce' technique to get a crisp, non-muddy sound. 2. Learn basic Latin off-beat rhythms.", "difficulty": "Beginner"},
    {"name": "Marimba", "culture": "Southern African", "type": "Percussion", "origin": "Africa/Central America", "emoji": "🎵", "description": "A percussion instrument consisting of a set of wooden bars struck with mallets, with resonators hanging below.", "playing": "Struck with yarn or rubber mallets. Can be played with 2 or 4 mallets (two in each hand).", "learning": "1. Master the 2-mallet stroke (bounce). 2. Learn the 'Stevens' or 'Burton' grip for 4-mallet playing.", "difficulty": "Intermediate"},
    {"name": "Mandolin", "culture": "European", "type": "String (Plucked)", "origin": "Italy", "emoji": "🎸", "description": "A stringed instrument of the lute family, featuring paired strings (courses).", "playing": "Plucked with a plectrum. Uses a rapid 'tremolo' technique to sustain notes.", "learning": "1. Learn basic chord shapes. 2. Master the tremolo picking technique.", "difficulty": "Beginner", "classification": "Chordophone"},
    {"name": "Marovany", "culture": "East African", "type": "String (Plucked)", "origin": "Madagascar", "emoji": "📦", "description": "A box-shaped zither from Madagascar.", "playing": "Plucked with the thumbs. The hands reach inside the wooden box to pluck the strings on both sides.", "learning": "1. Learn the alternate thumb plucking. 2. Master traditional Malagasy rhythms.", "difficulty": "Intermediate", "classification": "Chordophone", "fact": "The Marovany is a uniquely box-shaped zither from Madagascar, played by inserting the hands inside the resonating chamber."},
    {"name": "Masenqo", "culture": "East African", "type": "String (Bowed)", "origin": "Ethiopia", "emoji": "🎻", "description": "A single-stringed bowed lute from Ethiopia.", "playing": "Bowed with a horsehair bow. The string is pressed against the neck by the fingernails, similar to a Sarangi.", "learning": "1. Master the fingernail stopping technique. 2. Learn Ethiopian pentatonic scales.", "difficulty": "Advanced", "classification": "Chordophone", "fact": "The Masenqo is played by Azmaris (wandering Ethiopian musicians) who use it to improvise sung poetry."},
    {"name": "Mbira", "culture": "Southern African", "type": "Percussion (Lamellophone)", "origin": "Zimbabwe", "emoji": "👆", "description": "An African musical instrument, traditional to the Shona people of Zimbabwe. Consists of metal tines attached to a wooden board.", "playing": "Played by plucking the metal tines with the thumbs and right index finger. Often placed inside a large calabash (deze) for resonance.", "learning": "1. Learn the basic 'kushaura' (leading) part. 2. Understand the interlocking nature of Mbira music (kutsinhira).", "difficulty": "Intermediate"},
    {"name": "Mijwiz", "culture": "Middle East", "type": "Wind (Reed)", "origin": "Levant", "emoji": "🫛", "description": "A traditional Middle Eastern reed instrument made of two parallel bamboo tubes.", "playing": "Blown through a double reed. Both tubes are played simultaneously using circular breathing to create a continuous, hypnotic drone melody.", "learning": "1. Master circular breathing. 2. Learn the traditional fingerings for the specific Levantine maqams.", "difficulty": "Advanced"},
    {"name": "Molo", "culture": "West Africa", "type": "String (Plucked)", "origin": "Ghana", "emoji": "🎸", "description": "A two-stringed West African lute.", "playing": "Plucked with the fingers. Often plays rhythmic ostinato patterns to accompany singing.", "learning": "1. Learn the pentatonic tuning. 2. Master rhythmic strumming patterns.", "difficulty": "Beginner", "classification": "Chordophone", "fact": "The Molo is used by the Hausa and Dagomba people and is known for its twangy, rhythmic sound."},
    {"name": "Moraharpa", "culture": "Scandinavian", "type": "Wind (Free Reed)", "origin": "Sweden", "emoji": "🎹", "description": "An early Scandinavian keyed fipple/flute, an ancestor to the modern Nyckelharpa.", "playing": "Blown into while pressing keys to change the pitch. The keys press tangents against the string.", "learning": "1. Learn the basic key combinations. 2. Master Swedish folk tunes.", "difficulty": "Intermediate", "classification": "Aerophone", "fact": "The Moraharpa is an early predecessor to the modern nyckelharpa, featuring a bellows and keys."},
    {"name": "Morin Khuur", "culture": "Mongolian", "type": "String (Bowed)", "origin": "Mongolia", "emoji": "🐎", "description": "A traditional Mongolian bowed stringed instrument. The scroll is carved as a horse's head.", "playing": "Bowed with a horsehair bow. The strings are made of horsehair. Often played with the 4th finger muting strings to create harmonics.", "learning": "1. Learn to rosin and tighten the traditional horsehair bow. 2. Master the traditional overtone techniques.", "difficulty": "Advanced"},
    {"name": "Morsing", "culture": "India", "type": "Percussion (Lamellophone)", "origin": "India", "emoji": "👅", "description": "An Indian mouth harp. It consists of a metal frame with a flexible tongue in the middle.", "playing": "Placed in the mouth and the tongue is plucked. The player's mouth cavity acts as the resonator, changing pitch with vowel shapes.", "learning": "1. Learn to pluck rhythmically without hurting teeth. 2. Master changing mouth shapes to create melodic overtones.", "difficulty": "Beginner"},
    {"name": "Mridangam", "culture": "India", "type": "Percussion", "origin": "India", "emoji": "🥁", "description": "A percussion instrument from India of ancient origin. It is the primary rhythmic accompaniment in Carnatic music.", "playing": "A double-sided drum. Played with hands using complex finger combinations. The bass side requires a temporary paste of rice flour to achieve its deep tone.", "learning": "1. Learn the 'Sollukattu' (spoken syllables). 2. Translate syllables to hand strokes. 3. Master the 'Mora' (rhythmic phrase).", "difficulty": "Advanced"},
    {"name": "Native American Flute", "culture": "Native American", "type": "Wind", "origin": "North America", "emoji": "🪈", "description": "A front-blown, duct flute instrument.", "playing": "Blown directly into the end. It requires no special embouchure (lip shape) like a silver flute, making it easy to produce a tone.", "learning": "1. Learn the basic pentatonic scale (holes 1-4). 2. Practice breath control for smooth transitions. 3. Add traditional ornaments like trills.", "difficulty": "Beginner"},
    {"name": "Ney", "culture": "Middle East", "type": "Wind", "origin": "Persia", "emoji": "🪈", "description": "An end-blown flute prominent in Middle Eastern music.", "playing": "Blown across the sharp edge of the open end. Requires a specific 'lip lock' (embouchure) to direct air across the rim.", "learning": "1. Learn to produce a sound on the rim. 2. Master breath control for long phrases. 3. Learn the microtones of the Arabic/Maqam system.", "difficulty": "Advanced"},
    {"name": "Ngoni", "culture": "West Africa", "type": "String (Plucked)", "origin": "Mali", "emoji": "🎸", "description": "a string instrument made of wood or gourd covered with cow skin, ancestor to the banjo.", "playing": "Plucked with thumbs. Often plays fast melodic riffs in Wassoulou music.", "learning": "1. Learn repetitive pentatonic riffs. 2. Play along with vocalists to understand phrasing.", "difficulty": "Intermediate"},
    {"name": "Nyatiti", "culture": "East African", "type": "String (Plucked)", "origin": "Kenya", "emoji": "🎸", "description": "A five-to-eight stringed lyre from Kenya, traditionally played by the Luo people.", "playing": "Plucked with the thumb and index finger. The player often wears a metal ring (Gara) on the big toe to strike a soundboard for percussion.", "learning": "1. Learn the alternating thumb/index plucking pattern. 2. Coordinate foot percussion with the melody.", "difficulty": "Intermediate"},
    {"name": "Nyckelharpa", "culture": "Scandinavian", "type": "String (Bowed)", "origin": "Sweden", "emoji": "🎻", "description": "A traditional Swedish chordophone that uses keys to change the pitch.", "playing": "Bowed with the right hand. The left hand presses keys that press tangents against the strings to change pitch.", "learning": "1. Coordinate bowing with key-pressing. 2. Learn Swedish polskas (dance tunes).", "difficulty": "Advanced"},
    {"name": "Ocarina", "culture": "Mesoamerican", "type": "Wind", "origin": "Mesoamerica/China", "emoji": "🥔", "description": "A small wind instrument, typically shaped like an oval or animal, with holes for fingers.", "playing": "Blown into a mouthpiece. Pitch changes by covering combinations of holes. Size, not hole size, dictates pitch.", "learning": "1. Learn basic major scales. 2. Practice moving fingers simultaneously to avoid 'smeared' notes.", "difficulty": "Beginner"},
    {"name": "Oud", "culture": "Middle East", "type": "String (Plucked)", "origin": "Persia/Arabia", "emoji": "🎸", "description": "A short-neck lute-type, pear-shaped stringed instrument.", "playing": "Plucked with a long thin plectrum (risha). It has no frets, allowing for microtonal slides.", "learning": "1. Learn to hold the Oud and pick properly. 2. Master the Maqam (microtonal scales) system. 3. Learn the 'takasim' (improvisation).", "difficulty": "Intermediate"},
    {"name": "Pan Flute", "culture": "Andean", "type": "Wind", "origin": "Andes/Greece", "emoji": "🎶", "description": "A wind instrument consisting of multiple pipes of gradually increasing length.", "playing": "Blown across the top of the pipes. Pitch changes by moving the head to blow into different length pipes.", "learning": "1. Master blowing across the top to get a clear tone. 2. Learn to quickly tilt the head to hop between adjacent pipes.", "difficulty": "Beginner"},
    {"name": "Pipa", "culture": "China", "type": "String (Plucked)", "origin": "China/Middle East", "emoji": "🎸", "description": "A four-stringed Chinese musical instrument, sometimes called the Chinese lute.", "playing": "Plucked with fingernails or picks. Features rapid left-hand bending and right-hand 'tremolo' (lunzhi) techniques.", "learning": "1. Learn the 'lunzhi' rolling technique. 2. Master left-hand pitch bends and vibrato.", "difficulty": "Advanced"},
    {"name": "Psaltery", "culture": "European", "type": "String (Plucked)", "origin": "Europe/Middle East", "emoji": "🎶", "description": "A stringed instrument of the zither family, popular in the Middle Ages and Renaissance.", "playing": "Plucked with the fingers or a plectrum, or bowed with a bow. The strings are open and stretched across a flat soundboard.", "learning": "1. Learn the diatonic layout of the strings. 2. Master plucking melodies without hitting adjacent strings.", "difficulty": "Beginner", "classification": "Chordophone", "fact": "The Psaltery is mentioned in the Bible (Psalm 150) and was a common instrument in medieval religious and secular music."},
    {"name": "Qanun", "culture": "Middle East", "type": "String (Zither)", "origin": "Mesopotamia", "emoji": "🎶", "description": "A string instrument played as part of an ensemble, in much of the Middle East.", "playing": "Plucked with metal picks attached to the fingers. Features small levers (mandals) to change pitch during performance.", "learning": "1. Learn basic plucking patterns. 2. Master manipulating the mandals for microtonal changes.", "difficulty": "Advanced"},
    {"name": "Qilauti", "culture": "Inuit", "type": "Percussion", "origin": "Arctic North America", "emoji": "🥁", "description": "A traditional Inuit frame drum held by the rim and played from underneath.", "playing": "Held by the rim from underneath and struck on the edge/joint of the frame, causing the drum to bounce off the hand.", "learning": "1. Practice the unique 'bouncing' strike. 2. Coordinate with traditional Inuit throat singing.", "difficulty": "Intermediate"},
    {"name": "Qraqeb", "culture": "North African", "type": "Percussion", "origin": "Morocco", "emoji": "🔩", "description": "Large iron castanets used in traditional Gnawa music of North Africa.", "playing": "Held in pairs (one in each hand) and struck together to produce a loud, metallic clacking sound. Often plays complex cross-rhythms.", "learning": "1. Master the heavy wrist motion required. 2. Learn the specific Gnawa rhythmic patterns.", "difficulty": "Intermediate", "classification": "Idiophone", "fact": "Qraqeb are large iron castanets that mimic the sound of horse hooves and chains, reflecting the history of enslaved people in the Gnawa tradition."},
    {"name": "Rabab", "culture": "Middle East", "type": "String (Bowed)", "origin": "Afghanistan", "emoji": "🎸", "description": "An ancient Afghan bowed string instrument, often considered the ancestor of the Indian sarangi.", "playing": "Bowed with a horsehair bow. It has a deep, resonant body carved from a single piece of wood, usually mulberry.", "learning": "1. Learn the traditional Afghan scales. 2. Master the bowing pressure required for the thick strings.", "difficulty": "Advanced"},
    {"name": "Ravanahatha", "culture": "India", "type": "String (Bowed)", "origin": "India/Rajasthan", "emoji": "🎻", "description": "An ancient bowed string instrument used in Rajasthan.", "playing": "Bowed with a horsehair bow. Has a coconut shell resonator and two main strings, often with sympathetic strings.", "learning": "1. Learn the basic drone melodies. 2. Coordinate with traditional folk singing.", "difficulty": "Intermediate", "classification": "Chordophone", "fact": "According to legend, the Ravanahatha was created by Ravana, a figure in Hindu mythology, and is an ancestor to the modern violin."},
    {"name": "Riq", "culture": "Middle East", "type": "Percussion", "origin": "Egypt/Middle East", "emoji": "🪘", "description": "A type of tambourine used as a traditional instrument in Arabic music.", "playing": "Held in the weak hand and struck with the strong hand, or shaken. Has brass cymbals that can be dampened by the fingers.", "learning": "1. Learn the 'dum' (low) and 'tak' (high) strokes. 2. Master the 'shake' technique to hit the cymbals rhythmically.", "difficulty": "Intermediate"},
    {"name": "Santur", "culture": "Middle East", "type": "String (Struck)", "origin": "Persia", "emoji": "🔨", "description": "A trapezoid-shaped Iranian hammered dulcimer.", "playing": "Struck with two small, lightweight wooden mallets (mezrab) to play fast, cascading melodies.", "learning": "1. Coordinate the right and left mallets independently. 2. Learn the Persian Dastgah (modes) system.", "difficulty": "Advanced"},
    {"name": "Sarangi", "culture": "India", "type": "String (Bowed)", "origin": "India", "emoji": "🎻", "description": "A bowed, short-necked string instrument from India, known for its vocal-like sound.", "playing": "Bowed. The left hand does not press the strings, but presses *underneath* them against the fingernails to change pitch.", "learning": "1. Master the painful fingernail technique. 2. Learn Indian ragas and glissandos (meend).", "difficulty": "Advanced", "classification": "Chordophone"},
    {"name": "Saron", "culture": "Southeast Asian", "type": "Percussion", "origin": "Indonesia", "emoji": "🎵", "description": "A musical instrument of the gamelan ensemble, consisting of bronze bars laid over a wooden trough.", "playing": "Struck with a wooden or horn mallet. The player dampens the previous note with the free hand when striking the next.", "learning": "1. Learn the basic melody (balungan). 2. Master the dampening technique for clean, bell-like tones.", "difficulty": "Beginner"},
    {"name": "Serpent", "culture": "European", "type": "Wind (Reed-less)", "origin": "France", "emoji": "🐍", "description": "An ancient bass wind instrument made of wood covered in leather, shaped like a snake.", "playing": "Blown through a cup-shaped mouthpiece like a brass instrument, but features finger holes like a woodwind.", "learning": "1. Master the difficult brass embouchure. 2. Coordinate finger holes while maintaining pitch.", "difficulty": "Advanced", "classification": "Aerophone", "fact": "The Serpent was invented in 1590 to support Gregorian chanting in French churches, and is the evolutionary ancestor of the modern tuba."},
    {"name": "Setar", "culture": "Middle East", "type": "String (Plucked)", "origin": "Persia", "emoji": "🎸", "description": "A Persian lute with four strings, used in Persian classical music.", "playing": "Plucked with the index finger. The player presses the strings directly against the frets to create microtonal bends.", "learning": "1. Learn the 'Mezrab' (index finger plucking). 2. Master the Radif (Persian classical repertoire).", "difficulty": "Advanced", "classification": "Chordophone", "fact": "Despite its name meaning 'three strings' in Persian, the modern Setar has four strings."},
    {"name": "Shakuhachi", "culture": "Japan", "type": "Wind", "origin": "Japan", "emoji": "🪈", "description": "A traditional Japanese bamboo end-blown flute.", "playing": "Blown into the sharp, open end. Pitch is heavily manipulated by covering holes partially and changing head angle.", "learning": "1. Learn to produce a tone (very difficult). 2. Master the traditional 'Honkyoku' breathing techniques. 3. Practice 'meri' (bending notes).", "difficulty": "Advanced"},
    {"name": "Shamisen", "culture": "Japan", "type": "String (Plucked)", "origin": "Japan", "emoji": "🎸", "description": "A three-stringed traditional Japanese instrument derived from the Chinese sanxian.", "playing": "Plucked with a large plectrum (bachi). The neck is fretless, and the skin is struck to create a percussive 'thwack'.", "learning": "1. Learn the up-and-down bachi strokes. 2. Practice striking the skin for percussive effect. 3. Learn traditional Japanese scales.", "difficulty": "Intermediate"},
    {"name": "Shawm", "culture": "European", "type": "Wind (Reed)", "origin": "Europe/Middle East", "emoji": "🎺", "description": "A medieval and Renaissance double-reed woodwind instrument, predecessor to the oboe.", "playing": "Blown through a broad double reed. Fingers cover holes. Produces a loud, penetrating sound ideal for outdoor use.", "learning": "1. Build strong embouchure for the large reed. 2. Master Renaissance dance melodies.", "difficulty": "Intermediate", "classification": "Aerophone", "fact": "The Shawm was the standard outdoor double-reed instrument of the Middle Ages, and its loud, piercing sound made it the predecessor to the modern oboe."},
    {"name": "Sheng", "culture": "China", "type": "Wind (Reed)", "origin": "China", "emoji": "🫛", "description": "A Chinese mouth organ, consisting of a metal bowl with bamboo pipes of varying lengths.", "playing": "Blown into (exhaled and inhaled). Fingers cover holes on the pipes. It is designed to play multiple notes (chords) at once.", "learning": "1. Learn basic single-pipe melodies. 2. Practice playing intervals and chords by covering multiple holes.", "difficulty": "Intermediate"},
    {"name": "Shofar", "culture": "Middle Eastern", "type": "Wind", "origin": "Ancient Israel", "emoji": "🐑", "description": "An ancient musical horn typically made of a ram's horn, used for Jewish religious purposes.", "playing": "Blown like a brass instrument. Has no finger holes, only playing natural overtones.", "learning": "1. Learn the tight-lipped embouchure. 2. Master the specific religious calls (Tekiah, Shevarim, Teruah).", "difficulty": "Intermediate", "classification": "Aerophone"},
    {"name": "Singing Bowl", "culture": "Himalayan", "type": "Percussion", "origin": "Tibet/Nepal", "emoji": "🥣", "description": "A type of bell that vibrates and produces a rich, deep tone when struck or rubbed.", "playing": "Struck with a padded mallet, or rubbed around the rim with a wooden stick to create a continuous singing tone via friction.", "learning": "1. Practice the circular motion of the stick around the rim to sustain the tone. 2. Master maintaining even pressure.", "difficulty": "Beginner"},
    {"name": "Sintir", "culture": "North African", "type": "String (Plucked)", "origin": "Morocco", "emoji": "🎸", "description": "A three-stringed skin-covered bass plucked lute from Morocco.", "playing": "Plucked with the fingers. Often plays a repetitive, driving bassline and rhythm.", "learning": "1. Learn the pentatonic tuning. 2. Master the rhythmic 'Sintir' bounce.", "difficulty": "Intermediate", "classification": "Chordophone", "fact": "Also known as the Hajhuj, it is the backbone of Gnawa music, producing deep hypnotic basslines."},
    {"name": "Sitar", "culture": "India", "type": "String (Plucked)", "origin": "Indian Subcontinent", "emoji": "🪕", "description": "A plucked string instrument used in Hindustani classical music.", "playing": "Plucked with a wire plectrum (mizrab) on the index finger. Left hand pulls strings sideways across frets to bend pitch (meend).", "learning": "1. Learn to hold the instrument properly. 2. Master 'meend' (pitch bending). 3. Practice basic Raga scales (alap).", "difficulty": "Advanced"},
    {"name": "Sopila", "culture": "Balkan", "type": "Wind (Reed)", "origin": "Croatia", "emoji": "🎺", "description": "A traditional Croatian double-reed woodwind instrument.", "playing": "Blown through a double reed. Fingers cover holes. Produces a loud, nasal tone used in Istrian music.", "learning": "1. Build embouchure for the double reed. 2. Master the Istrian scale, which uses microtones.", "difficulty": "Advanced", "classification": "Aerophone"},
    {"name": "Sralai", "culture": "Southeast Asian", "type": "Wind (Reed)", "origin": "Cambodia", "emoji": "🎺", "description": "A wind instrument used in the pinpeat ensemble of Cambodia.", "playing": "Blown through a quadruple reed. Fingers cover holes. Produces a loud, piercing sound similar to the oboe.", "learning": "1. Master the breath control for the thick reed. 2. Learn the specific melodic patterns of pinpeat music.", "difficulty": "Advanced"},
    {"name": "Steelpan", "culture": "Caribbean", "type": "Percussion", "origin": "Trinidad and Tobago", "emoji": "🛢️", "description": "A musical instrument originating from Trinidad and Tobago, made from 55-gallon industrial drums.", "playing": "Struck with rubber-tipped sticks. Different sizes/areas of the concave bowl produce different pitches.", "learning": "1. Memorize the layout of notes on the pan. 2. Practice stroke technique (bouncing off the metal). 3. Learn Calypso rhythms.", "difficulty": "Intermediate"},
    {"name": "Suling", "culture": "Southeast Asian", "type": "Wind", "origin": "Indonesia", "emoji": "🪈", "description": "A bamboo flute used in Balinese and Javanese gamelan ensembles.", "playing": "Blown into the end. Features 4 holes. Uses circular breathing to maintain continuous melodies.", "learning": "1. Learn the 4-hole fingering. 2. Master circular breathing for sustained notes.", "difficulty": "Beginner", "classification": "Aerophone"},
    {"name": "Suona", "culture": "China", "type": "Wind (Reed)", "origin": "China/Middle East", "emoji": "🎺", "description": "A Chinese double-reed horn. It has a distinctively loud and high-pitched sound.", "playing": "Blown with a small, stiff double reed. Fingers cover holes on a conical wooden body. A brass bell amplifies the sound.", "learning": "1. Learn circular breathing to sustain the loud tone. 2. Master traditional ornamentation and trills.", "difficulty": "Intermediate"},
    {"name": "Tabla", "culture": "India", "type": "Percussion", "origin": "India", "emoji": "🥁", "description": "A pair of twin hand drums used in traditional and classical music of the Indian subcontinent.", "playing": "The smaller drum (Dayan) is played with fingertips. The larger drum (Bayan) uses the whole hand and wrist. Features complex 'bols' (syllables).", "learning": "1. Learn the basic bols (Na, Tin, Ga, Dha). 2. Master the 'Kayda' (theme and variations) structure.", "difficulty": "Advanced"},
    {"name": "Taiko", "culture": "Japan", "type": "Percussion", "origin": "Japan/China", "emoji": "🥁", "description": "A broad range of Japanese percussion instruments, specifically the cylindrical wadaiko.", "playing": "Struck with wooden sticks (bachi) in a wide, martial-arts-like stance. Emphasizes stance, ki (energy), and powerful strikes.", "learning": "1. Learn the proper stance and grip. 2. Master basic rhythmic patterns. 3. Practice the 'kiai' (shout) to maintain energy.", "difficulty": "Intermediate"},
    {"name": "Talking Drum", "culture": "West Africa", "type": "Percussion", "origin": "West Africa", "emoji": "🗣️", "description": "An hourglass drum from West Africa whose pitch can mimic human speech.", "playing": "Held under the arm and struck with a curved stick. Squeezing the leather ropes tightens the heads, raising the pitch.", "learning": "1. Coordinate squeezing and striking. 2. Learn traditional proverbs translated into drum language.", "difficulty": "Intermediate"},
    {"name": "Tamburica", "culture": "Balkan", "type": "String (Plucked)", "origin": "Croatia/Serbia", "emoji": "🎸", "description": "A family of string instruments popular in the folk music of Croatia, Serbia, and Hungary.", "playing": "Plucked with a plectrum or fingers. Often played in orchestras (tamburica orchestras) with different sizes covering bass, chord, and melody.", "learning": "1. Learn tremolo technique. 2. Understand the role of your specific tamburica in the ensemble.", "difficulty": "Intermediate"},
    {"name": "Tangmuri", "culture": "India", "type": "Wind (Reed)", "origin": "India (Meghalaya)", "emoji": "🎺", "description": "A traditional double-reed instrument from the Khasi people of Meghalaya.", "playing": "Blown through a double reed. Fingers cover holes. Produces a loud, piercing sound.", "learning": "1. Learn breath control. 2. Master traditional Khasi melodies.", "difficulty": "Intermediate", "classification": "Aerophone", "fact": "The Tangmuri is the lead instrument in traditional Khasi religious and ceremonial music."},
    {"name": "Tar", "culture": "Middle East", "type": "String (Plucked)", "origin": "Persia", "emoji": "🎸", "description": "An Iranian long-necked lute with a double-bowl shaped body, traditionally carved from mulberry wood.", "playing": "Plucked with a brass plectrum (mezrab). Has 6 strings in 3 courses. The neck has movable frets tied on for microtones.", "learning": "1. Learn to tie and adjust the frets for the specific Dastgah (mode) you are playing. 2. Master rapid mezrab techniques.", "difficulty": "Advanced"},
    {"name": "Tarka", "culture": "Andean", "type": "Wind", "origin": "Bolivia/Peru", "emoji": "🪈", "description": "A unique vertical flute of the Andes, made of wood, with a block flute mouthpiece.", "playing": "Blown into a mouthpiece. Has a dark, breathy, wooden sound. Played in ensembles during festivals.", "learning": "1. Learn breath pressure to get a clean tone. 2. Master traditional Andean festival tunes.", "difficulty": "Intermediate", "classification": "Aerophone"},
    {"name": "Tarogato", "culture": "European", "type": "Wind (Reed)", "origin": "Hungary", "emoji": "🪈", "description": "A Hungarian woodwind instrument with a conical bore and a double reed.", "playing": "Blown through a reed. Fingers cover holes. Has a dark, mournful, and penetrating tone.", "learning": "1. Master reed control. 2. Learn traditional Hungarian military and folk tunes.", "difficulty": "Advanced"},
    {"name": "Theorbo", "culture": "European", "type": "String (Plucked)", "origin": "Italy", "emoji": "🎸", "description": "A large member of the lute family, featuring an extended neck for long bass strings.", "playing": "Plucked with the fingers. The right hand plays the main strings, while the extended bass strings are plucked for drones.", "learning": "1. Learn to navigate the massive fretboard. 2. Master playing basslines and melodies simultaneously.", "difficulty": "Advanced", "classification": "Chordophone", "fact": "The Theorbo was developed in the late 16th century specifically to accompany the voice, featuring a second pegbox for extremely long bass strings."},
    {"name": "Tin Whistle", "culture": "Celtic", "type": "Wind", "origin": "Ireland", "emoji": "🪈", "description": "A simple six-holed woodwind instrument, a type of fipple flute.", "playing": "Blown directly into the mouthpiece. Fingers cover six holes. Pitch is bent by sliding fingers off holes or blowing harder.", "learning": "1. Learn the D major scale. 2. Master traditional Irish ornaments (cuts, taps, and rolls). 3. Play jigs and reels.", "difficulty": "Beginner"},
    {"name": "Tonkori", "culture": "Japanese", "type": "String (Plucked)", "origin": "Japan (Ainu)", "emoji": "🎸", "description": "A plucked string instrument played by the Ainu people of northern Japan.", "playing": "Plucked with the fingers. Has 5 strings and no frets. Often plays a steady drone with melodic notes on top.", "learning": "1. Learn the open tunings. 2. Practice the alternating drone/melody plucking pattern.", "difficulty": "Intermediate"},
    {"name": "Tovshuur", "culture": "Mongolian", "type": "String (Plucked)", "origin": "Mongolia", "emoji": "🎸", "description": "A two-stringed lute used in Mongolian traditional music, often accompanying throat singing.", "playing": "Plucked or strummed. The neck is fretless.", "learning": "1. Learn basic rhythmic strumming patterns. 2. Coordinate with Altai throat singing styles.", "difficulty": "Beginner"},
    {"name": "Trembita", "culture": "Eastern European", "type": "Wind", "origin": "Ukraine (Carpathians)", "emoji": "📯", "description": "A traditional Ukrainian alpine horn made of wood.", "playing": "Blown like a brass instrument. Has no finger holes. Used by Hutsul shepherds for communication in the mountains.", "learning": "1. Learn the brass embouchure. 2. Master breath control to hit specific overtones.", "difficulty": "Intermediate", "classification": "Aerophone", "fact": "Trembitas can be up to 4 meters (13 feet) long, making them some of the longest wind instruments in the world."},
    {"name": "Tres", "culture": "Caribbean/Latin", "type": "String (Plucked)", "origin": "Cuba", "emoji": "🎸", "description": "A Cuban stringed instrument, similar to a guitar but with three sets of double strings.", "playing": "Plucked with a pick or fingers. The tuning is unique, and it is the primary melodic instrument in Cuban Son music.", "learning": "1. Learn the unique re-entrant tuning. 2. Master the 'montuno' pattern (syncopated melodic strumming).", "difficulty": "Intermediate"},
    {"name": "Tro", "culture": "Southeast Asian", "type": "String (Bowed)", "origin": "Cambodia", "emoji": "🎻", "description": "A traditional Cambodian bowed string instrument.", "playing": "Bowed vertically on the knee. Has a soundbox made of coconut shell.", "learning": "1. Learn traditional Khmer tuning. 2. Master the specific bowing technique.", "difficulty": "Advanced", "classification": "Chordophone", "fact": "The Tro is essential to the pinpeat orchestras of Cambodia, often playing intricate melodic lines."},
    {"name": "Tsabouna", "culture": "European", "type": "Wind (Reed)", "origin": "Greece", "emoji": "🫛", "description": "A traditional Greek bagpipe made from a whole goatskin.", "playing": "Air is blown into the goatskin bag, which feeds a double reed chanter. Has no drones, just the melody pipe.", "learning": "1. Master maintaining pressure on the bag. 2. Learn traditional Greek island dance melodies.", "difficulty": "Advanced", "classification": "Aerophone", "fact": "The Tsabouna is a Greek bagpipe made from the entire skin of a goat, where the legs are tied off and the neck is used as the blowpipe."},
    {"name": "Tsvirurl", "culture": "Aboriginal Australian", "type": "Wind", "origin": "Northern Australia", "emoji": "🪈", "description": "A traditional Aboriginal Australian didgeridoo, typically made from termite-hollowed eucalyptus.", "playing": "Played with vibrating lips. Requires 'circular breathing'. Often decorated with traditional ochre designs.", "learning": "1. Learn circular breathing. 2. Incorporate diaphragm pulses and vocalizations.", "difficulty": "Intermediate"},
    {"name": "Tsuzumi", "culture": "Japan", "type": "Percussion", "origin": "Japan", "emoji": "🥁", "description": "A Japanese hourglass drum of Indian/Chinese origin, used in Noh and Kabuki theater.", "playing": "Struck with the fingers. The player squeezes the tension ropes to change the pitch of the drumhead while striking.", "learning": "1. Master the squeeze-and-strike technique. 2. Learn the specific 'kakegoe' (shouts) that accompany the strikes.", "difficulty": "Advanced"},
    {"name": "Tupan", "culture": "Balkan", "type": "Percussion", "origin": "Balkans/Middle East", "emoji": "🥁", "description": "A large double-headed drum played with a heavy mallet and a thin stick.", "playing": "Played with a heavy mallet (dum) on one side and a thin stick (tak) on the other. Sling over shoulder for marching.", "learning": "1. Coordinate the heavy mallet and thin stick. 2. Learn uneven Balkan rhythms (e.g., 7/8, 9/8 time).", "difficulty": "Advanced"},
    {"name": "Txalaparta", "culture": "European", "type": "Percussion", "origin": "Basque Country", "emoji": "🪵", "description": "a specialized Basque music device of wood or stone. ", "playing": "Two performers strike thick wooden boards resting on baskets. They improvise rhythms, alternating beats in a call-and-response style.", "learning": "1. Find a partner to practice call-and-response. 2. Learn to maintain the 'ttakuna' and 'herrena' beat pattern.", "difficulty": "Beginner"},
    {"name": "Txistu", "culture": "European", "type": "Wind", "origin": "Basque Country", "emoji": "🪈", "description": "A Basque fipple flute, traditionally played with one hand.", "playing": "Blown directly into. Played one-handed so the player can play a drum (tamboril) with the other hand.", "learning": "1. Master the one-handed fingering system. 2. Coordinate playing the flute with a drum strapped to your arm.", "difficulty": "Intermediate"},
    {"name": "Uilleann Pipes", "culture": "Celtic", "type": "Wind (Reed)", "origin": "Ireland", "emoji": "🎷", "description": "The characteristic national bagpipe of Ireland, played by pumping air with a bellows under the arm.", "playing": "Air is pumped via a bellows under the right arm. The left hand plays the chanter (melody), the right hand plays regulators (chord drones).", "learning": "1. Coordinate the bellows pumping. 2. Learn chanter melodies. 3. Add regulator chords with the wrist.", "difficulty": "Advanced"},
    {"name": "Ukulele", "culture": "Polynesian", "type": "String (Plucked)", "origin": "Hawaii/Portugal", "emoji": "🎸", "description": "A small lute family instrument developed in Hawaii based on the Portuguese machete.", "playing": "Strummed or plucked with fingers. Standard tuning is GCEA, often with the G string tuned higher than the C (re-entrant tuning).", "learning": "1. Learn 4-5 basic open chords (C, G, Am, F). 2. Master the traditional Hawaiian 'chunk' strum. 3. Learn standard chord progressions.", "difficulty": "Beginner"},
    {"name": "Valiha", "culture": "East African", "type": "String (Plucked)", "origin": "Madagascar", "emoji": "🎋", "description": "A tubular zither from Madagascar made from a single piece of bamboo.", "playing": "Plucked with the fingers. The strings are made from fibers of the bamboo itself, lifted off the body on small bridges.", "learning": "1. Learn the traditional tunings. 2. Master the intertwining polyphonic style of Malagasy music.", "difficulty": "Intermediate", "classification": "Chordophone", "fact": "The Valiha is considered the national instrument of Madagascar, and remarkably, its strings are made from the bamboo tube itself rather than separate materials."},
    {"name": "Veena", "culture": "India", "type": "String (Plucked)", "origin": "India", "emoji": "🎶", "description": "A plucked musical instrument with a long fretted neck and two large gourds acting as resonators.", "playing": "Plucked with fingers. Has a small gourd attached to the neck that rests on the player's left shoulder.", "learning": "1. Learn to pull the strings laterally for 'meend' (glissando). 2. Practice playing the 'tala' (rhythm) on the drone strings.", "difficulty": "Advanced"},
    {"name": "Vielle", "culture": "European", "type": "String (Bowed)", "origin": "France/Europe", "emoji": "🎻", "description": "A European bowed stringed instrument used in the Medieval period, a predecessor to the violin.", "playing": "Bowed with an archery-style bow. It usually has 5 strings, one of which is a drone string off the side of the neck.", "learning": "1. Learn to manage the drone string while bowing. 2. Study Medieval dance melodies (Estampie).", "difficulty": "Intermediate"},
    {"name": "Viola Caipira", "culture": "South American", "type": "String (Plucked)", "origin": "Brazil", "emoji": "🎸", "description": "A ten-string guitar from Brazil, used in traditional folklore and country music.", "playing": "Plucked with the fingers. Has 5 courses of paired strings. Often uses alternative tunings to fit the singer's voice.", "learning": "1. Learn the standard 'Cebolão' tuning. 2. Master the rasgueado strumming patterns.", "difficulty": "Intermediate", "classification": "Chordophone", "fact": "Despite being called a 'viola', this Brazilian instrument is actually a guitar with 10 strings paired in 5 courses, central to rural folklore music."},
    {"name": "Washboard", "culture": "North American", "type": "Percussion", "origin": "USA", "emoji": "🧺", "description": "A musical instrument adapted from the household washing tool, used in jug bands and zydeco.", "playing": "Worn on the chest and scraped with thimbles on the fingers, or struck with small wooden sticks.", "learning": "1. Master the thimble scraping technique. 2. Learn basic Zydeco or old-time rhythms.", "difficulty": "Beginner"},
    {"name": "Washint", "culture": "East African", "type": "Wind", "origin": "Ethiopia", "emoji": "🪈", "description": "An end-blown Ethiopian flute with four finger holes.", "playing": "Blown across the rim. Typically has 4 holes. Used in Ethiopian traditional music alongside the masenqo and krar.", "learning": "1. Learn the traditional Ethiopian pentatonic scales (Kignit). 2. Master breath control to bend notes.", "difficulty": "Intermediate"},
    {"name": "Washtub Bass", "culture": "North American", "type": "String (Plucked)", "origin": "USA", "emoji": "🪣", "description": "A stringed instrument that uses a metal washtub as a resonator.", "playing": "A broomstick is attached to the tub, with a string running to the top. The player changes pitch by moving the stick to change string tension.", "learning": "1. Learn to feel the pitch change as you bend the stick. 2. Lock into the rhythm of a guitarist or banjo player.", "difficulty": "Beginner"},
    {"name": "Water Drum", "culture": "Native American", "type": "Percussion", "origin": "North America", "emoji": "💧", "description": "A drum used by Native Americans made by filling a kettle with water and placing a hide over it.", "playing": "The water inside tunes the drumhead. Struck with a padded stick. The water creates a unique, sloshing resonance.", "learning": "1. Learn to tune the drum by adjusting water levels. 2. Practice traditional Iroquois or Navajo social dance songs.", "difficulty": "Intermediate"},
    {"name": "Xiao", "culture": "China", "type": "Wind", "origin": "China", "emoji": "🪈", "description": "A traditional Chinese end-blown bamboo flute, known for its soft, melancholic tone.", "playing": "Blown across the notch at the top end. Features 5 to 8 finger holes. Pitch is bent by partially covering holes and altering breath.", "learning": "1. Learn the breath angle to produce a clean tone. 2. Master the traditional 'dianyin' (ornamentation) techniques.", "difficulty": "Intermediate", "classification": "Aerophone", "fact": "The Xiao is an ancient Chinese end-blown flute historically favored by scholars and monks for its quiet, meditative, and melancholic tone."},
    {"name": "Xun", "culture": "China", "type": "Wind", "origin": "China", "emoji": "🥔", "description": "A vessel flute (globular flute) made of clay or ceramic, originating in ancient China.", "playing": "Blown into a mouthpiece on the top. Fingers cover holes on the sides. It produces a rich, muffled, and melancholy tone.", "learning": "1. Learn the specific breath angle required for a clean tone. 2. Master the traditional Chinese pentatonic scales.", "difficulty": "Intermediate"},
    {"name": "Yaybahar", "culture": "European/Modern", "type": "String (Friction)", "origin": "Turkey", "emoji": "🎛️", "description": "A modern acoustic electronic-sounding instrument invented by Görkem Şen.", "playing": "Played by sliding a coiled spring and striking drum heads, which resonate strings. It sounds like a digital synth but is entirely acoustic.", "learning": "1. Learn to bow the springs. 2. Coordinate the drum head strikes.", "difficulty": "Advanced", "classification": "Chordophone", "fact": "The Yaybahar was invented in 2014 and produces cinematic, sci-fi soundscapes despite being entirely acoustic."},
    {"name": "Yueqin", "culture": "China", "type": "String (Plucked)", "origin": "China", "emoji": "🌙", "description": "A traditional Chinese lute with a round wooden body and a short neck.", "playing": "Plucked with a plectrum or fingers. Named 'moon lute' due to its circular soundbox.", "learning": "1. Learn basic chord shapes. 2. Practice playing melodic lines in the Peking opera style.", "difficulty": "Intermediate"},
    {"name": "Zarb", "culture": "Middle East", "type": "Percussion", "origin": "Persia", "emoji": "🥁", "description": "A Persian goblet drum, also known as a Tonbak.", "playing": "Played with the fingers and palms. Features a highly developed technique of rolls, snaps, and strikes.", "learning": "1. Learn the 'Tom' (bass) and 'Bak' (snap). 2. Master the Persian rhythmic cycles.", "difficulty": "Advanced", "classification": "Membranophone", "fact": "The Zarb is the chief percussion instrument of Persian classical music, capable of imitating spoken language."},
    {"name": "Zhaleika", "culture": "Russian", "type": "Wind (Reed)", "origin": "Russia", "emoji": "🎺", "description": "A Russian single-reed horn.", "playing": "Blown through a single reed with a cow horn bell. Fingers cover holes.", "learning": "1. Learn to control the reed. 2. Master Russian folk tunes.", "difficulty": "Beginner", "classification": "Aerophone", "fact": "The Zhaleika is known for its melancholic, piercing sound and is also called the 'weeping horn'."},
    {"name": "Zither", "culture": "European", "type": "String (Plucked)", "origin": "Alpine Europe", "emoji": "🎶", "description": "A stringed instrument whose strings are stretched across a flat, thin body.", "playing": "Melody strings (near the player) are fretted with the left hand and plucked with a thumb ring on the right. Accompaniment strings are plucked by fingers.", "learning": "1. Coordinate the thumb ring with left-hand fretting. 2. Learn Alpine folk melodies.", "difficulty": "Intermediate"},
    {"name": "Zurna", "culture": "Middle East", "type": "Wind (Reed)", "origin": "Turkey/Persia", "emoji": "🎺", "description": "A double-reed outdoor wind instrument with a bright, piercing sound.", "playing": "Blown through a disc lip-rest with a double reed. Fingers cover holes. Often played alongside the davul (bass drum).", "learning": "1. Learn circular breathing. 2. Master the ornaments and trills specific to Turkish folk music.", "difficulty": "Advanced"}
]
# Sort alphabetically by name
INSTRUMENTS_DATA = sorted(INSTRUMENTS_DATA, key=lambda x: x['name'])

# --- Stylesheets ---
LIGHT_STYLE = """
    QMainWindow { background-color: #ffffff; }
    QTabWidget::pane { border: 1px solid #ddd; border-radius: 5px; top: -1px; }
    QTabBar::tab { background: #f0f0f0; border: 1px solid #ddd; padding: 8px 20px; border-top-left-radius: 4px; border-top-right-radius: 4px; }
    QTabBar::tab:selected { background: #fff; border-bottom: none; font-weight: bold; color: #0066cc; }
    QListWidget { font-size: 14px; border: 1px solid #ddd; border-radius: 5px; background-color: #fff; }
    QListWidget::item { padding: 10px; border-bottom: 1px solid #eee; color: #333; }
    QListWidget::item:selected { background-color: #0066cc; color: white; }
    QLineEdit, QComboBox { padding: 6px; font-size: 14px; border: 1px solid #ccc; border-radius: 4px; background-color: #fff; color: #333; }
    QComboBox QAbstractItemView { background-color: #fff; color: #333; selection-background-color: #0066cc; }
    QCheckBox { font-size: 13px; color: #333; }
    QPushButton { padding: 8px 16px; font-size: 13px; border: 1px solid #ccc; border-radius: 4px; background-color: #f0f0f0; color: #333; }
    QPushButton:hover { background-color: #e0e0e0; }
    #DetailPanel { background-color: #f9f9f9; border-radius: 5px; }
    #QuizButton { padding: 20px; font-size: 16px; font-weight: bold; background-color: #e6f2ff; border: 2px solid #0066cc; border-radius: 8px; }
    #QuizButton:hover { background-color: #cce6ff; }
    #QuizButton:pressed { background-color: #b3d9ff; }
    #ScoreLabel { font-size: 18px; font-weight: bold; color: #333; }
    #SubHeader { font-size: 16px; font-weight: bold; color: #0066cc; margin-top: 10px; }
    #StatusBar { color: #666; font-size: 12px; padding: 5px; }
    #StatsText { font-size: 15px; color: #333; }
    #Flashcard { background-color: #f9f9f9; border: 2px solid #0066cc; border-radius: 15px; padding: 20px; }
    #FlashcardLabel { font-size: 18px; color: #333; }
"""

DARK_STYLE = """
    QMainWindow { background-color: #1e1e1e; }
    QTabWidget::pane { border: 1px solid #444; border-radius: 5px; top: -1px; }
    QTabBar::tab { background: #2b2b2b; border: 1px solid #444; padding: 8px 20px; border-top-left-radius: 4px; border-top-right-radius: 4px; color: #aaa; }
    QTabBar::tab:selected { background: #1e1e1e; border-bottom: none; font-weight: bold; color: #4da6ff; }
    QListWidget { font-size: 14px; border: 1px solid #444; border-radius: 5px; background-color: #2b2b2b; color: #eee; }
    QListWidget::item { padding: 10px; border-bottom: 1px solid #3a3a3a; color: #eee; }
    QListWidget::item:selected { background-color: #0066cc; color: white; }
    QLineEdit, QComboBox { padding: 6px; font-size: 14px; border: 1px solid #555; border-radius: 4px; background-color: #333; color: #eee; }
    QComboBox QAbstractItemView { background-color: #333; color: #eee; selection-background-color: #0066cc; }
    QCheckBox { font-size: 13px; color: #eee; }
    QPushButton { padding: 8px 16px; font-size: 13px; border: 1px solid #555; border-radius: 4px; background-color: #3a3a3a; color: #eee; }
    QPushButton:hover { background-color: #4a4a4a; }
    #DetailPanel { background-color: #252525; border-radius: 5px; }
    #QuizButton { padding: 20px; font-size: 16px; font-weight: bold; background-color: #2a3b4d; border: 2px solid #4da6ff; border-radius: 8px; color: #fff; }
    #QuizButton:hover { background-color: #345080; }
    #QuizButton:pressed { background-color: #1e2e40; }
    #ScoreLabel { font-size: 18px; font-weight: bold; color: #eee; }
    #SubHeader { font-size: 16px; font-weight: bold; color: #4da6ff; margin-top: 10px; }
    #StatusBar { color: #888; font-size: 12px; padding: 5px; }
    #StatsText { font-size: 15px; color: #eee; }
    #Flashcard { background-color: #252525; border: 2px solid #4da6ff; border-radius: 15px; padding: 20px; }
    #FlashcardLabel { font-size: 18px; color: #eee; }
"""

class InstrumentExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("World Instruments Explorer v13")
        self.resize(1100, 750)
        
        # Initialize State
        self.instruments = INSTRUMENTS_DATA
        self.is_dark_mode = False
        self.show_favorites_only = False
        self.score = 0
        self.questions_asked = 0
        self.recently_viewed = []
        self.flashcard_index = 0
        self.flashcard_revealed = False
        
        # Initialize favorites and backfill missing classifications
        for inst in self.instruments:
            inst['favorite'] = False
            
            # Auto-backfill Hornbostel-Sachs Classification if missing
            if 'classification' not in inst:
                if "String" in inst['type']:
                    inst['classification'] = "Chordophone"
                elif "Wind" in inst['type']:
                    inst['classification'] = "Aerophone"
                elif "Lamellophone" in inst['type']:
                    inst['classification'] = "Idiophone"
                else:
                    # Default membranophone for general percussion
                    inst['classification'] = "Membranophone"
            
            # Auto-backfill Difficulty if missing
            if 'difficulty' not in inst:
                inst['difficulty'] = "Unknown"

            # Auto-backfill Fact if missing
            if 'fact' not in inst:
                inst['fact'] = f"The {inst['name']} is a fascinating instrument with deep roots in {inst['culture']} culture."

        self.setup_ui()
        self.populate_filters()
        self.update_list()
        self.apply_theme()
        self.start_new_quiz_question()
        self.update_stats_tab()
        self.setup_shortcuts()
        self.update_flashcard()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Top Bar ---
        top_bar = QWidget()
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(15, 10, 15, 10)
        
        title = QLabel("🌍 World Instruments Explorer")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        
        self.theme_btn = QPushButton("🌙 Dark Mode")
        self.theme_btn.clicked.connect(self.toggle_theme)

        top_bar_layout.addWidget(title)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.theme_btn)
        main_layout.addWidget(top_bar)

        # --- Tabs ---
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.setup_explore_tab()
        self.setup_quiz_tab()
        self.setup_stats_tab()
        self.setup_flashcard_tab()

    def setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+F"), self, activated=self.search_bar.setFocus)
        QShortcut(QKeySequence("Ctrl+R"), self, activated=self.select_random_instrument)
        QShortcut(QKeySequence("Ctrl+B"), self, activated=self.toggle_theme)
        
        # Quiz shortcuts
        QShortcut(QKeySequence("1"), self, activated=lambda: self.trigger_quiz_btn(0))
        QShortcut(QKeySequence("2"), self, activated=lambda: self.trigger_quiz_btn(1))
        QShortcut(QKeySequence("3"), self, activated=lambda: self.trigger_quiz_btn(2))
        QShortcut(QKeySequence("4"), self, activated=lambda: self.trigger_quiz_btn(3))
        
        # Flashcard shortcut
        QShortcut(QKeySequence(Qt.Key_Space), self, activated=self.reveal_flashcard)

    def trigger_quiz_btn(self, idx):
        if self.tabs.currentIndex() == 1: # Only trigger if on Quiz tab
            if self.quiz_buttons[idx].isEnabled():
                self.quiz_buttons[idx].click()

    def setup_explore_tab(self):
        explore_widget = QWidget()
        layout = QVBoxLayout(explore_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # --- Top Controls ---
        top_controls = QHBoxLayout()
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by name, culture, type, or description...")
        self.search_bar.textChanged.connect(self.update_list)

        self.recent_combo = QComboBox()
        self.recent_combo.addItem("Recently Viewed...")
        self.recent_combo.currentIndexChanged.connect(self.select_recent)
        
        self.culture_combo = QComboBox()
        self.culture_combo.currentIndexChanged.connect(self.update_list)

        self.type_combo = QComboBox()
        self.type_combo.currentIndexChanged.connect(self.update_list)

        self.class_combo = QComboBox()
        self.class_combo.currentIndexChanged.connect(self.update_list)

        self.diff_combo = QComboBox()
        self.diff_combo.currentIndexChanged.connect(self.update_list)

        self.fav_checkbox = QCheckBox("★ Favorites Only")
        self.fav_checkbox.stateChanged.connect(self.toggle_favorites_filter)

        self.random_btn = QPushButton("🎲 Surprise Me!")
        self.random_btn.clicked.connect(self.select_random_instrument)

        top_controls.addWidget(self.search_bar, 3)
        top_controls.addWidget(self.recent_combo, 2)
        top_controls.addWidget(self.culture_combo, 2)
        top_controls.addWidget(self.type_combo, 2)
        top_controls.addWidget(self.class_combo, 2)
        top_controls.addWidget(self.diff_combo, 2)
        top_controls.addWidget(self.fav_checkbox, 1)
        top_controls.addWidget(self.random_btn, 1)
        layout.addLayout(top_controls)

        # --- Bottom Controls (Sort & Status) ---
        bottom_controls = QHBoxLayout()
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Sort by: Name", "Sort by: Culture", "Sort by: Type"])
        self.sort_combo.currentIndexChanged.connect(self.update_list)
        
        self.reset_btn = QPushButton("🔄 Reset Filters")
        self.reset_btn.clicked.connect(self.reset_filters)
        
        self.export_btn = QPushButton("📤 Export Favorites")
        self.export_btn.clicked.connect=self.export_favorites # Typo fix below
        
        self.status_label = QLabel(f"Showing {len(self.instruments)} of {len(self.instruments)} instruments")
        self.status_label.setObjectName("StatusBar")
        
        bottom_controls.addWidget(self.sort_combo)
        bottom_controls.addWidget(self.reset_btn)
        bottom_controls.addWidget(self.export_btn)
        bottom_controls.addStretch()
        bottom_controls.addWidget(self.status_label)
        layout.addLayout(bottom_controls)

        # --- Splitter ---
        splitter = QSplitter(Qt.Horizontal)

        # Left: List
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        self.instrument_list = QListWidget()
        self.instrument_list.currentRowChanged.connect(self.display_details)
        left_layout.addWidget(self.instrument_list)

        # Right: Details in a Scroll Area
        self.detail_panel = QFrame()
        self.detail_panel.setObjectName("DetailPanel")
        right_layout = QVBoxLayout(self.detail_panel)
        right_layout.setContentsMargins(20, 20, 20, 20)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setAlignment(Qt.AlignTop)
        scroll_layout.setSpacing(10)

        self.title_label = QLabel("Select an Instrument")
        self.title_label.setStyleSheet("font-size: 26px; font-weight: bold;")
        self.title_label.setWordWrap(True)

        self.meta_label = QLabel("")
        self.meta_label.setStyleSheet("font-size: 14px; margin-bottom: 5px;")
        self.meta_label.setWordWrap(True)
        
        self.desc_label = QLabel("")
        self.desc_label.setStyleSheet("font-size: 16px;")
        self.desc_label.setWordWrap(True)
        self.desc_label.setAlignment(Qt.AlignTop)

        self.howto_header = QLabel("🖐️ How It Is Played")
        self.howto_header.setObjectName("SubHeader")
        self.howto_label = QLabel("")
        self.howto_label.setStyleSheet("font-size: 15px;")
        self.howto_label.setWordWrap(True)
        self.howto_label.setAlignment(Qt.AlignTop)

        self.learn_header = QLabel("🎓 Learning Path")
        self.learn_header.setObjectName("SubHeader")
        self.learn_label = QLabel("")
        self.learn_label.setStyleSheet("font-size: 15px;")
        self.learn_label.setWordWrap(True)
        self.learn_label.setAlignment(Qt.AlignTop)

        self.fact_header = QLabel("💡 Fun Fact")
        self.fact_header.setObjectName("SubHeader")
        self.fact_label = QLabel("")
        self.fact_label.setStyleSheet("font-size: 15px; font-style: italic;")
        self.fact_label.setWordWrap(True)
        self.fact_label.setAlignment(Qt.AlignTop)

        scroll_layout.addWidget(self.title_label)
        scroll_layout.addWidget(self.meta_label)
        scroll_layout.addWidget(self.desc_label)
        scroll_layout.addWidget(self.howto_header)
        scroll_layout.addWidget(self.howto_label)
        scroll_layout.addWidget(self.learn_header)
        scroll_layout.addWidget(self.learn_label)
        scroll_layout.addWidget(self.fact_header)
        scroll_layout.addWidget(self.fact_label)
        scroll_layout.addStretch()

        scroll_area.setWidget(scroll_content)
        right_layout.addWidget(scroll_area)

        # Bottom controls of the details panel
        bottom_bar = QHBoxLayout()
        
        self.copy_btn = QPushButton("📋 Copy Details")
        self.copy_btn.clicked.connect(self.copy_details_to_clipboard)

        self.culture_btn = QPushButton("🌍 More from this Culture")
        self.culture_btn.clicked.connect(self.filter_by_current_culture)

        self.listen_btn = QPushButton("🎵 Listen (YouTube)")
        self.listen_btn.clicked.connect(self.listen_on_youtube)
        
        self.watch_btn = QPushButton("🎓 Watch Lessons (YouTube)")
        self.watch_btn.clicked.connect(self.watch_lessons_on_youtube)

        self.fav_btn = QPushButton("☆ Add to Favorites")
        self.fav_btn.setFixedWidth(160)
        self.fav_btn.clicked.connect(self.toggle_current_favorite)

        bottom_bar.addWidget(self.copy_btn)
        bottom_bar.addWidget(self.culture_btn)
        bottom_bar.addWidget(self.listen_btn)
        bottom_bar.addWidget(self.watch_btn)
        bottom_bar.addStretch()
        bottom_bar.addWidget(self.fav_btn)
        
        right_layout.addLayout(bottom_bar)

        splitter.addWidget(left_panel)
        splitter.addWidget(self.detail_panel)
        splitter.setSizes([350, 750])
        layout.addWidget(splitter)
        
        self.tabs.addTab(explore_widget, "📖 Explore")

    def setup_quiz_tab(self):
        quiz_widget = QWidget()
        layout = QVBoxLayout(quiz_widget)
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.setSpacing(20)

        self.score_label = QLabel("Score: 0 / 0")
        self.score_label.setObjectName("ScoreLabel")
        self.score_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.score_label)

        self.quiz_question_label = QLabel("Loading question...")
        self.quiz_question_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.quiz_question_label.setWordWrap(True)
        self.quiz_question_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.quiz_question_label)

        self.quiz_desc_label = QLabel("")
        self.quiz_desc_label.setStyleSheet("font-size: 16px; font-style: italic;")
        self.quiz_desc_label.setWordWrap(True)
        self.quiz_desc_label.setAlignment(Qt.AlignCenter)
        self.quiz_desc_label.setMinimumHeight(80)
        layout.addWidget(self.quiz_desc_label)

        self.quiz_buttons = []
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        
        positions = [(i, j) for i in range(2) for j in range(2)]
        for pos in positions:
            btn = QPushButton()
            btn.setObjectName("QuizButton")
            btn.setMinimumHeight(60)
            btn.clicked.connect(lambda checked, b=btn: self.check_quiz_answer(b))
            grid_layout.addWidget(btn, pos[0], pos[1])
            self.quiz_buttons.append(btn)
            
        layout.addLayout(grid_layout)
        
        self.next_q_btn = QPushButton("Next Question ➡️")
        self.next_q_btn.setFixedWidth(200)
        self.next_q_btn.clicked.connect(self.start_new_quiz_question)
        layout.addWidget(self.next_q_btn, alignment=Qt.AlignCenter)

        self.tabs.addTab(quiz_widget, "🧠 Quiz")

    def setup_stats_tab(self):
        stats_widget = QWidget()
        layout = QVBoxLayout(stats_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setAlignment(Qt.AlignTop)
        
        self.stats_label = QLabel("Calculating statistics...")
        self.stats_label.setObjectName("StatsText")
        self.stats_label.setWordWrap(True)
        self.stats_label.setAlignment(Qt.AlignTop)
        content_layout.addWidget(self.stats_label)
        
        scroll_area.setWidget(content)
        layout.addWidget(scroll_area)
        
        self.tabs.addTab(stats_widget, "📊 Stats")

    def setup_flashcard_tab(self):
        fc_widget = QWidget()
        layout = QVBoxLayout(fc_widget)
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.setSpacing(20)
        
        self.flashcard_frame = QFrame()
        self.flashcard_frame.setObjectName("Flashcard")
        self.flashcard_frame.setMinimumHeight(400)
        self.flashcard_frame.setMaximumWidth(600)
        
        fc_layout = QVBoxLayout(self.flashcard_frame)
        fc_layout.setAlignment(Qt.AlignCenter)
        
        self.fc_emoji_label = QLabel("🎸")
        self.fc_emoji_label.setStyleSheet("font-size: 80px;")
        self.fc_emoji_label.setAlignment(Qt.AlignCenter)
        
        self.fc_type_label = QLabel("String (Plucked)")
        self.fc_type_label.setObjectName("FlashcardLabel")
        self.fc_type_label.setAlignment(Qt.AlignCenter)
        
        self.fc_culture_label = QLabel("Andean")
        self.fc_culture_label.setObjectName("FlashcardLabel")
        self.fc_culture_label.setAlignment(Qt.AlignCenter)
        
        self.fc_separator = QLabel("─" * 30)
        self.fc_separator.setStyleSheet("color: #ccc;")
        self.fc_separator.setAlignment(Qt.AlignCenter)
        
        self.fc_desc_label = QLabel("Description goes here...")
        self.fc_desc_label.setObjectName("FlashcardLabel")
        self.fc_desc_label.setWordWrap(True)
        self.fc_desc_label.setAlignment(Qt.AlignCenter)
        
        self.fc_answer_label = QLabel("❓")
        self.fc_answer_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #0066cc;")
        self.fc_answer_label.setAlignment(Qt.AlignCenter)
        
        fc_layout.addWidget(self.fc_emoji_label)
        fc_layout.addWidget(self.fc_type_label)
        fc_layout.addWidget(self.fc_culture_label)
        fc_layout.addWidget(self.fc_separator)
        fc_layout.addWidget(self.fc_desc_label)
        fc_layout.addWidget(self.fc_answer_label)
        
        layout.addWidget(self.flashcard_frame)
        
        fc_controls = QHBoxLayout()
        fc_controls.setAlignment(Qt.AlignCenter)
        
        self.fc_prev_btn = QPushButton("⬅️ Previous")
        self.fc_prev_btn.clicked.connect(self.prev_flashcard)
        
        self.fc_reveal_btn = QPushButton("👁️ Reveal Answer (Space)")
        self.fc_reveal_btn.clicked.connect(self.reveal_flashcard)
        
        self.fc_next_btn = QPushButton("Next ➡️")
        self.fc_next_btn.clicked.connect(self.next_flashcard)
        
        fc_controls.addWidget(self.fc_prev_btn)
        fc_controls.addWidget(self.fc_reveal_btn)
        fc_controls.addWidget(self.fc_next_btn)
        
        layout.addLayout(fc_controls)
        
        self.tabs.addTab(fc_widget, "📇 Flashcards")

    # --- Explore Tab Logic ---
    def populate_filters(self):
        cultures = sorted(list(set(inst['culture'] for inst in self.instruments)))
        types = sorted(list(set(inst['type'] for inst in self.instruments)))
        classes = sorted(list(set(inst['classification'] for inst in self.instruments)))
        diffs = sorted(list(set(inst['difficulty'] for inst in self.instruments)))

        self.culture_combo.clear()
        self.culture_combo.addItem("All Cultures")
        self.culture_combo.addItems(cultures)

        self.type_combo.clear()
        self.type_combo.addItem("All Types")
        self.type_combo.addItems(types)

        self.class_combo.clear()
        self.class_combo.addItem("All Classes")
        self.class_combo.addItems(classes)

        self.diff_combo.clear()
        self.diff_combo.addItem("All Difficulties")
        self.diff_combo.addItems(diffs)

    def update_list(self):
        search_text = self.search_bar.text().lower()
        culture_filter = self.culture_combo.currentText()
        type_filter = self.type_combo.currentText()
        class_filter = self.class_combo.currentText()
        diff_filter = self.diff_combo.currentText()
        sort_mode = self.sort_combo.currentText()

        # Sort logic
        if "Culture" in sort_mode:
            sorted_insts = sorted(self.instruments, key=lambda x: (x['culture'], x['name']))
        elif "Type" in sort_mode:
            sorted_insts = sorted(self.instruments, key=lambda x: (x['type'], x['name']))
        else:
            sorted_insts = sorted(self.instruments, key=lambda x: x['name'])

        self.filtered_instruments = []
        
        for inst in sorted_insts:
            if self.show_favorites_only and not inst.get('favorite', False):
                continue
                
            # Deep Search: Search across multiple fields
            searchable_text = f"{inst['name']} {inst['culture']} {inst['type']} {inst['description']} {inst['playing']} {inst['learning']} {inst.get('fact', '')}".lower()
            if search_text not in searchable_text:
                continue
                
            if culture_filter != "All Cultures" and inst['culture'] != culture_filter:
                continue
            if type_filter != "All Types" and inst['type'] != type_filter:
                continue
            if class_filter != "All Classes" and inst['classification'] != class_filter:
                continue
            if diff_filter != "All Difficulties" and inst['difficulty'] != diff_filter:
                continue
                
            self.filtered_instruments.append(inst)

        self.instrument_list.clear()
        for inst in self.filtered_instruments:
            fav = "★ " if inst.get('favorite', False) else ""
            display_text = f"{fav}{inst['emoji']}  {inst['name']}  ({inst['culture']})"
            self.instrument_list.addItem(display_text)
            
        self.status_label.setText(f"Showing {len(self.filtered_instruments)} of {len(self.instruments)} instruments")
            
        if self.filtered_instruments:
            self.instrument_list.setCurrentRow(0)
        else:
            self.clear_details()

    def highlight_text(self, text, search):
        if not search or len(search) < 3:
            return text
        pattern = re.compile(f"({re.escape(search)})", re.IGNORECASE)
        return pattern.sub(r"<b style='background-color: #ffeb3b; color: #000;'>\1</b>", text)

    def select_random_instrument(self):
        if not self.filtered_instruments:
            return
        random_index = random.randint(0, len(self.filtered_instruments) - 1)
        self.instrument_list.setCurrentRow(random_index)

    def reset_filters(self):
        self.search_bar.clear()
        self.culture_combo.setCurrentIndex(0)
        self.type_combo.setCurrentIndex(0)
        self.class_combo.setCurrentIndex(0)
        self.diff_combo.setCurrentIndex(0)
        self.sort_combo.setCurrentIndex(0)
        self.fav_checkbox.setChecked(False)

    def export_favorites(self):
        favs = [inst for inst in self.instruments if inst.get('favorite', False)]
        if not favs:
            QMessageBox.information(self, "No Favorites", "You have no favorite instruments to export.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Export Favorites", "my_favorite_instruments.txt", "Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    for inst in favs:
                        f.write(f"{inst['emoji']} {inst['name']} ({inst['culture']})\n")
                        f.write(f"Type: {inst['type']} | Classification: {inst['classification']} | Difficulty: {inst['difficulty']}\n")
                        f.write(f"Description: {inst['description']}\n")
                        f.write(f"Fun Fact: {inst['fact']}\n")
                        f.write("-" * 50 + "\n")
                QMessageBox.information(self, "Export Successful", f"Successfully exported {len(favs)} favorites to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to save file:\n{e}")

    def display_details(self, index):
        if index < 0 or index >= len(self.filtered_instruments):
            return
            
        inst = self.filtered_instruments[index]
        
        # Update recently viewed
        self.update_recently_viewed(inst)
        
        self.title_label.setText(f"{inst['emoji']} {inst['name']}")
        meta_html = f"<b>Type:</b> {inst['type']} &nbsp;|&nbsp; <b>Origin:</b> {inst['origin']} &nbsp;|&nbsp; <b>Culture:</b> {inst['culture']}<br><b>Classification:</b> {inst['classification']} &nbsp;|&nbsp; <b>Difficulty:</b> {inst['difficulty']}"
        self.meta_label.setText(meta_html)
        
        search_text = self.search_bar.text().strip()
        desc_html = self.highlight_text(inst['description'], search_text)
        howto_html = self.highlight_text(inst['playing'], search_text)
        
        desc_color = "#ccc" if self.is_dark_mode else "#333"
        sub_color = "#aaa" if self.is_dark_mode else "#555"
        fact_color = "#888" if self.is_dark_mode else "#777"
        self.desc_label.setText(f"<div style='color: {desc_color};'>{desc_html}</div>")
        self.howto_label.setText(f"<div style='color: {sub_color};'>{howto_html}</div>")
        self.learn_label.setText(f"<div style='color: {sub_color};'>{inst['learning']}</div>")
        self.fact_label.setText(f"<div style='color: {fact_color};'>{inst['fact']}</div>")
        
        self.update_fav_button(inst)

    def update_recently_viewed(self, inst):
        if inst in self.recently_viewed:
            self.recently_viewed.remove(inst)
        self.recently_viewed.insert(0, inst)
        self.recently_viewed = self.recently_viewed[:5] # Keep max 5
        
        self.recent_combo.blockSignals(True)
        self.recent_combo.clear()
        self.recent_combo.addItem("Recently Viewed...")
        for i in self.recently_viewed:
            self.recent_combo.addItem(f"{i['emoji']} {i['name']}")
        self.recent_combo.blockSignals(False)

    def select_recent(self, idx):
        if idx <= 0:
            return
        inst = self.recently_viewed[idx-1]
        # Find this instrument in the filtered list and select it
        for i, f_inst in enumerate(self.filtered_instruments):
            if f_inst == inst:
                self.instrument_list.setCurrentRow(i)
                break

    def copy_details_to_clipboard(self):
        if not self.filtered_instruments or self.instrument_list.currentRow() < 0:
            return
        inst = self.filtered_instruments[self.instrument_list.currentRow()]
        text = f"INSTRUMENT: {inst['name']}\nCULTURE: {inst['culture']}\nTYPE: {inst['type']}\nCLASSIFICATION: {inst['classification']}\nDIFFICULTY: {inst['difficulty']}\n\nDESCRIPTION:\n{inst['description']}\n\nHOW IT IS PLAYED:\n{inst['playing']}\n\nLEARNING PATH:\n{inst['learning']}\n\nFUN FACT:\n{inst['fact']}"
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(text)

    def filter_by_current_culture(self):
        if not self.filtered_instruments or self.instrument_list.currentRow() < 0:
            return
        inst = self.filtered_instruments[self.instrument_list.currentRow()]
        culture = inst['culture']
        
        index = self.culture_combo.findText(culture)
        if index != -1:
            self.culture_combo.setCurrentIndex(index)

    def listen_on_youtube(self):
        if not self.filtered_instruments or self.instrument_list.currentRow() < 0:
            return
        inst = self.filtered_instruments[self.instrument_list.currentRow()]
        search_query = f"{inst['name']} instrument music"
        url = QUrl(f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}")
        QDesktopServices.openUrl(url)
        
    def watch_lessons_on_youtube(self):
        if not self.filtered_instruments or self.instrument_list.currentRow() < 0:
            return
        inst = self.filtered_instruments[self.instrument_list.currentRow()]
        search_query = f"how to play {inst['name']} instrument lessons"
        url = QUrl(f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}")
        QDesktopServices.openUrl(url)

    def update_fav_button(self, inst):
        if inst.get('favorite', False):
            self.fav_btn.setText("★ Favorited")
        else:
            self.fav_btn.setText("☆ Add to Favorites")

    def toggle_current_favorite(self):
        if not self.filtered_instruments or self.instrument_list.currentRow() < 0:
            return
        inst = self.filtered_instruments[self.instrument_list.currentRow()]
        inst['favorite'] = not inst.get('favorite', False)
        self.update_list() 
        self.display_details(self.instrument_list.currentRow()) 

    def toggle_favorites_filter(self, state):
        self.show_favorites_only = bool(state)
        self.update_list()

    def clear_details(self):
        self.title_label.setText("No instruments found")
        self.meta_label.setText("")
        self.desc_label.setText("Try adjusting your search or filters.")
        self.howto_label.setText("")
        self.learn_label.setText("")
        self.fact_label.setText("")
        self.fav_btn.setText("☆ Add to Favorites")

    # --- Quiz Tab Logic ---
    def start_new_quiz_question(self):
        for btn in self.quiz_buttons:
            btn.setStyleSheet("")
            btn.setEnabled(True)
        self.next_q_btn.setEnabled(False)

        self.current_quiz_answer = random.choice(self.instruments)
        distractors = random.sample([i for i in self.instruments if i != self.current_quiz_answer], 3)
        options = distractors + [self.current_quiz_answer]
        random.shuffle(options)
        
        for i, btn in enumerate(self.quiz_buttons):
            opt = options[i]
            btn.setText(f"{opt['emoji']} {opt['name']}")
            btn.instrument_ref = opt

        self.quiz_question_label.setText("Which instrument matches this description?")
        self.quiz_desc_label.setText(f'"{self.current_quiz_answer["description"]}"')

    def check_quiz_answer(self, clicked_btn):
        for btn in self.quiz_buttons:
            btn.setEnabled(False)
            
        self.questions_asked += 1
        
        if clicked_btn.instrument_ref == self.current_quiz_answer:
            clicked_btn.setStyleSheet("background-color: #4CAF50; color: white; border: 2px solid #2E7D32;")
            self.score += 1
        else:
            clicked_btn.setStyleSheet("background-color: #F44336; color: white; border: 2px solid #C62828;")
            for btn in self.quiz_buttons:
                if btn.instrument_ref == self.current_quiz_answer:
                    btn.setStyleSheet("background-color: #4CAF50; color: white; border: 2px solid #2E7D32;")

        self.score_label.setText(f"Score: {self.score} / {self.questions_asked}")
        self.next_q_btn.setEnabled(True)

    # --- Flashcard Tab Logic ---
    def update_flashcard(self):
        if not self.instruments:
            return
        inst = self.instruments[self.flashcard_index]
        
        self.fc_emoji_label.setText(inst['emoji'])
        self.fc_type_label.setText(f"Type: {inst['type']}")
        self.fc_culture_label.setText(f"Culture: {inst['culture']}")
        self.fc_desc_label.setText(inst['description'])
        
        if self.flashcard_revealed:
            self.fc_answer_label.setText(f"✅ {inst['name']}")
        else:
            self.fc_answer_label.setText("❓")

    def reveal_flashcard(self):
        self.flashcard_revealed = True
        self.update_flashcard()

    def next_flashcard(self):
        self.flashcard_revealed = False
        self.flashcard_index = (self.flashcard_index + 1) % len(self.instruments)
        self.update_flashcard()

    def prev_flashcard(self):
        self.flashcard_revealed = False
        self.flashcard_index = (self.flashcard_index - 1 + len(self.instruments)) % len(self.instruments)
        self.update_flashcard()

    # --- Stats Tab Logic ---
    def update_stats_tab(self):
        total = len(self.instruments)
        cultures = {}
        types = {}
        classes = {}
        diffs = {}
        
        for i in self.instruments:
            cultures[i['culture']] = cultures.get(i['culture'], 0) + 1
            types[i['type']] = types.get(i['type'], 0) + 1
            classes[i['classification']] = classes.get(i['classification'], 0) + 1
            diffs[i['difficulty']] = diffs.get(i['difficulty'], 0) + 1
            
        header_color = "#4da6ff" if self.is_dark_mode else "#0066cc"
        text_color = "#eee" if self.is_dark_mode else "#333"
        
        html = f"<h2 style='color: {header_color};'>Database Statistics</h2>"
        html += f"<div style='color: {text_color};'><b>Total Instruments:</b> {total}<br><br>"
        
        html += f"<b style='color: {header_color};'>By Classification:</b><br>"
        for k, v in sorted(classes.items(), key=lambda item: item[1], reverse=True):
            html += f"&nbsp;&nbsp;{k}: {v}<br>"
            
        html += f"<br><b style='color: {header_color};'>By Difficulty:</b><br>"
        for k, v in sorted(diffs.items(), key=lambda item: item[1], reverse=True):
            html += f"&nbsp;&nbsp;{k}: {v}<br>"
            
        html += f"<br><b style='color: {header_color};'>By Culture:</b><br>"
        for k, v in sorted(cultures.items(), key=lambda item: item[1], reverse=True):
            html += f"&nbsp;&nbsp;{k}: {v}<br>"
            
        html += f"<br><b style='color: {header_color};'>By Type:</b><br>"
        for k, v in sorted(types.items(), key=lambda item: item[1], reverse=True):
            html += f"&nbsp;&nbsp;{k}: {v}<br>"
            
        html += "</div>"
        self.stats_label.setText(html)

    # --- Theme Logic ---
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()
        self.update_stats_tab() # Update stats colors

    def apply_theme(self):
        if self.is_dark_mode:
            self.setStyleSheet(DARK_STYLE)
            self.theme_btn.setText("☀️ Light Mode")
            self.title_label.setStyleSheet("font-size: 26px; font-weight: bold; color: #4da6ff;")
            self.meta_label.setStyleSheet("font-size: 14px; color: #999; margin-bottom: 5px;")
            self.desc_label.setStyleSheet("font-size: 16px; color: #ccc;")
            self.howto_label.setStyleSheet("font-size: 15px; color: #aaa;")
            self.learn_label.setStyleSheet("font-size: 15px; color: #aaa;")
            self.fact_label.setStyleSheet("font-size: 15px; color: #888; font-style: italic;")
            self.fc_answer_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #4da6ff;")
        else:
            self.setStyleSheet(LIGHT_STYLE)
            self.theme_btn.setText("🌙 Dark Mode")
            self.title_label.setStyleSheet("font-size: 26px; font-weight: bold; color: #0066cc;")
            self.meta_label.setStyleSheet("font-size: 14px; color: #666; margin-bottom: 5px;")
            self.desc_label.setStyleSheet("font-size: 16px; color: #333;")
            self.howto_label.setStyleSheet("font-size: 15px; color: #555;")
            self.learn_label.setStyleSheet("font-size: 15px; color: #555;")
            self.fact_label.setStyleSheet("font-size: 15px; color: #777; font-style: italic;")
            self.fc_answer_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #0066cc;")
            
        if self.filtered_instruments:
            self.display_details(self.instrument_list.currentRow())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    font = app.font()
    font.setFamily("Segoe UI")
    font.setPointSize(10)
    app.setFont(font)

    window = InstrumentExplorer()
    window.show()
    sys.exit(app.exec())