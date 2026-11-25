"""Hand curation for Story of America. Omega-written, never part of the reading text.

TIMELINE: one entry per chapter for the family timeline Page (year label plus a short event line).
CONTENT: severity overrides and "reading it today" notes (approved by Omega Games, Nov 24, 2026).
Severity: none, low, medium, high. Rules in scripts/scan.py set a default; entries here override it.
"""

TIMELINE = {
 1: ("about 1000", "Norse sailors reach Vinland"), 2: ("1484 to 1492", "Columbus seeks a way west"),
 3: ("1492", "Columbus reaches the Caribbean"), 4: ("1493", "Columbus returns to Spain"),
 5: ("1507", "The name America appears on a map"), 6: ("1497", "John Cabot reaches North America"),
 7: ("1562", "French Huguenots reach Florida"), 8: ("1564", "The French build Fort Caroline"),
 9: ("1565", "Spain takes Fort Caroline"), 10: ("1568", "Dominique de Gourgues strikes back"),
 11: ("1583", "Humphrey Gilbert claims Newfoundland"), 12: ("1584 to 1590", "The Roanoke colonies"),
 13: ("1607", "Jamestown is founded"), 14: ("1608", "John Smith leads Jamestown"),
 15: ("1609 to 1614", "The Starving Time, then peace"), 16: ("1616", "Pocahontas travels to England"),
 17: ("1622", "War between the Powhatan people and the colony"), 18: ("1619 to 1624", "Virginia's assembly and charter"),
 19: ("1640s", "Royalist Cavaliers come to Virginia"), 20: ("1676", "Bacon's Rebellion"),
 21: ("1716", "The Knights of the Golden Horseshoe ride west"), 22: ("1620", "The Pilgrims land at Plymouth"),
 23: ("1630", "Massachusetts Bay is founded"), 24: ("1636", "Harry Vane governs Massachusetts"),
 25: ("1638", "Anne Hutchinson and Rhode Island"), 26: ("1636", "Harvard is founded"),
 27: ("1656", "Quakers arrive in New England"), 28: ("1620s", "Maine and New Hampshire are settled"),
 29: ("1636 to 1637", "Connecticut is founded; the Pequot War"), 30: ("1638", "New Haven is founded"),
 31: ("1660 to 1661", "The hunt for the regicides"), 32: ("1675 to 1676", "King Philip's War"),
 33: ("1687", "The Charter Oak"), 34: ("1692", "The Salem witch trials"),
 35: ("1634", "Maryland is founded"), 36: ("1664", "New Amsterdam becomes New York"),
 37: ("1689 to 1691", "Leisler rules New York"), 38: ("1690s", "Pirates and Captain Kidd"),
 39: ("1664", "New Jersey is founded"), 40: ("1681 to 1682", "William Penn founds Pennsylvania"),
 41: ("1723", "Benjamin Franklin comes to Philadelphia"), 42: ("1663 to 1670", "The Carolinas are founded"),
 43: ("1711 to 1715", "The Tuscarora and Yamasee Wars"), 44: ("1733", "Georgia is founded"),
 45: ("1673 to 1682", "Marquette, Joliet and La Salle on the Mississippi"), 46: ("1689 to 1713", "King William's and Queen Anne's Wars"),
 47: ("1717 to 1720", "The Mississippi Bubble"), 48: ("1755", "Braddock's defeat"),
 49: ("1759 to 1763", "Quebec falls and French rule ends"), 50: ("1763", "Pontiac's War"),
 51: ("1773", "The Boston Tea Party"), 52: ("1775", "Paul Revere's ride, Lexington and Concord"),
 53: ("1775", "Bunker Hill"), 54: ("1775 to 1776", "The war in Canada"),
 55: ("1776", "The Declaration of Independence"), 56: ("1776 to 1777", "Trenton and Princeton"),
 57: ("1777", "Bennington and Oriskany"), 58: ("1777", "Saratoga"),
 59: ("1777 to 1778", "Brandywine, Germantown and Valley Forge"), 60: ("1779", "John Paul Jones and the war at sea"),
 61: ("1778", "Monmouth and Molly Pitcher"), 62: ("1780", "Benedict Arnold's treason"),
 63: ("1781", "Victory at Yorktown"), 64: ("1789 to 1797", "Washington is President"),
 65: ("1797 to 1801", "John Adams keeps peace with France"), 66: ("1803", "The Louisiana Purchase"),
 67: ("1804 to 1806", "Lewis and Clark"), 68: ("1806 to 1807", "Aaron Burr's plot"),
 69: ("1811", "Tecumseh, the Prophet and Tippecanoe"), 70: ("1812 to 1815", "The War of 1812"),
 71: ("1820 to 1823", "The Missouri Compromise and the Monroe Doctrine"), 72: ("1828", "The Tariff of Abominations"),
 73: ("1829 to 1841", "Jackson, nullification and hard times"), 74: ("1841", "Harrison, the hero of Tippecanoe"),
 75: ("1845", "Florida becomes a state"), 76: ("1845 to 1848", "Texas and the Mexican War"),
 77: ("1848", "Gold in California"), 78: ("1850", "The Compromise of 1850"),
 79: ("1850", "The Underground Railroad"), 80: ("1854 to 1856", "Bleeding Kansas"),
 81: ("1857 to 1858", "The Utah War"), 82: ("1858 to 1861", "Lincoln, secession and Fort Sumter"),
 83: ("1861 to 1862", "Bull Run to Fort Donelson"), 84: ("1862", "The first battle of ironclads"),
 85: ("1862", "Shiloh and New Orleans"), 86: ("1863", "The Emancipation Proclamation"),
 87: ("1863", "Chancellorsville"), 88: ("1863", "Gettysburg"),
 89: ("1864", "Grant's campaign and Sheridan's ride"), 90: ("1864", "Sherman's march; Lincoln re-elected"),
 91: ("1865", "The war ends; Lincoln is killed"), 92: ("1865 to 1868", "Reconstruction and Johnson's impeachment"),
 93: ("1872", "A peaceful settlement with Britain"), 94: ("1877 to 1885", "Hayes, Garfield and Arthur"),
 95: ("1885 to 1897", "Cleveland, Harrison, Cleveland"), 96: ("1898 to 1901", "War with Spain; McKinley is killed"),
 97: ("1901 to 1913", "Roosevelt and Taft"), 98: ("1913 to 1916", "Troubles with Mexico"),
 99: ("1917", "America enters the Great War"),
}

# "Reading it today" notes (approved Nov 24, 2026). Plain, short, for a grown-up to read before the chapter.
NATIVE = ("This book was written in 1917. It often calls Native Americans \"savages\" or \"Redmen\" and tells events "
          "mostly from the settlers' side. Today we say Native Americans or use each nation's own name, and we know "
          "these nations were defending their homes and land.")
SLAVERY_TERM = ("This book was written in 1917 and uses old words for Black Americans that we don't use today. "
                "Today we say Black Americans or enslaved people.")
VIOLENCE = "This chapter has battle or war scenes. You may want to read it first."

CONTENT = {
 # HIGH
 "tcoo-13-3": ("high", ["native_framing", "violence", "accuracy"],
   NATIVE + " The rescue by Pocahontas is told as fact; historians are not sure it happened as Smith told it."),
 "tcoo-14-2": ("medium", ["native_framing"], NATIVE),
 "tcoo-15-3": ("medium", ["native_framing", "accuracy"],
   NATIVE + " Pocahontas was taken captive by the English here; the book tells it as a fair bargain."),
 "tcoo-17-1": ("high", ["native_framing", "violence"],
   NATIVE + " This chapter tells the 1622 attack on the colony as treachery and leaves out why the Powhatan people "
   "were losing their land. The chapter title uses an old word too."),
 "tcoo-29-2": ("high", ["native_framing", "violence"],
   NATIVE + " The Pequot War ended with the English burning a Pequot village at Mystic, where hundreds of people died."),
 "tcoo-32-1": ("high", ["native_framing", "violence"],
   NATIVE + " King Philip (Metacom) was fighting to keep his people's land. This chapter has frightening raid scenes."),
 "tcoo-43-1": ("high", ["native_framing", "violence"],
   NATIVE + " It calls the Tuscarora \"crafty\"; they were going to war over stolen land and enslaved family members. "
   "This chapter has frightening attack scenes."),
 "tcoo-50-1": ("high", ["native_framing", "violence"],
   NATIVE + " Pontiac was an Odawa leader trying to stop British rule over his people's land."),
 "tcoo-50-2": ("high", ["native_framing", "violence"],
   NATIVE + " Pontiac was an Odawa leader trying to stop British rule over his people's land."),
 "tcoo-69-1": ("high", ["native_framing", "violence"],
   NATIVE + " Tecumseh was a Shawnee leader uniting nations to keep their land. A war speech in this chapter is frightening."),
 "tcoo-81-1": ("high", ["religion"],
   "This book was written in 1917. It speaks unkindly about Joseph Smith and the Latter-day Saints, a church with "
   "millions of members today. It tells their story only from their opponents' side."),
 "tcoo-92-1": ("high", ["race", "accuracy"],
   SLAVERY_TERM + " This chapter says newly freed Black voters were ignorant and that Reconstruction was a wretched time. "
   "Historians today disagree: Black Americans voted, served in Congress and helped rebuild the South, and the "
   "end of Reconstruction took many of those rights away."),
 "tcoo-09-2": ("high", ["violence"],
   "This chapter tells how Spanish soldiers killed French prisoners who had surrendered. It is upsetting; you may want to read it first."),
 "tcoo-10-1": ("high", ["violence", "native_framing"],
   "This chapter is about revenge: prisoners are hanged and soldiers are killed in battle. " + NATIVE),
 "tcoo-01-2": ("medium", ["native_framing", "violence"],
   "This book was written in 1917. It calls the Native people the Norse met \"savages.\" Today we say Native Americans. There is a short battle."),
 "ffs-27": ("low", ["slavery"], None),
 # MEDIUM: slavery framing and accuracy
 "tcoo-42-1": ("medium", ["slavery", "accuracy"],
   SLAVERY_TERM + " It says \"no one saw anything wrong\" with the slave trade. The enslaved people did, and some others did too."),
 "tcoo-71-1": ("medium", ["slavery", "accuracy"],
   "It says that at first \"no one thought slavery was wrong.\" The enslaved people always knew it was wrong, and some others said so too."),
 "tcoo-79-1": ("medium", ["slavery", "race"],
   SLAVERY_TERM + " It mentions Uncle Tom's Cabin and calls the character Topsy funny; that character is now seen as a hurtful stereotype."),
 "tcoo-82-1": ("medium", ["slavery"], SLAVERY_TERM + " It describes a slave market, where families were split up and sold."),
 "tcoo-86-1": ("medium", ["slavery", "violence"], SLAVERY_TERM + " " + VIOLENCE),
 "tcoo-64-3": ("low", ["slavery"], SLAVERY_TERM),
 "tcoo-34-1": ("medium", ["violence"], "This chapter tells how people accused of witchcraft in Salem were put to death. You may want to read it first."),
 "tcoo-03-2": ("medium", ["native_framing", "accuracy"],
   NATIVE + " Columbus and his men later enslaved many of the Taíno people they met."),
}

NATIVE_NOTE = NATIVE
SLAVERY_TOPIC_NOTE = ("This chapter talks about slavery and the long fight over it. Enslaved people were held and "
                      "sold against their will; it is a good chapter to talk through together.")
SLAVERY_NOTE = SLAVERY_TERM
VIOLENCE_NOTE = VIOLENCE

# One-line summaries in Omega's own words, shown when a family skips a high reading.
SKIP_SUMMARY = {
 "tcoo-09-2": "The Spanish leader Menéndez caught the French who had survived in Florida; many who surrendered were killed, and Spain kept Florida.",
 "tcoo-10-1": "A Frenchman, Dominique de Gourgues, sailed to Florida, took the Spanish forts with Native allies to avenge his countrymen, and went home to France.",
 "tcoo-13-3": "John Smith was captured by Powhatan's warriors while exploring, was brought before the great chief, and was later sent back to Jamestown.",
 "tcoo-17-1": "After years of peace, the Powhatan people, losing more and more of their land, attacked the Virginia settlements in 1622, and a long, hard war followed.",
 "tcoo-29-2": "The English colonists of Connecticut went to war with the Pequot people in 1637, and the war ended with a Pequot village destroyed and the Pequot nation broken apart.",
 "tcoo-32-1": "Metacom, called King Philip by the English, led a war to stop settlers taking his people's land; after a year of fighting on both sides he was killed and the war ended.",
 "tcoo-43-1": "The Carolinas quarreled with their governors, fought wars with the Tuscarora and Yamasee nations, and afterward became royal colonies.",
 "tcoo-50-1": "After France lost Canada, the Odawa leader Pontiac planned to drive the British from the forts on his people's land, and a young Native woman warned the fort at Detroit.",
 "tcoo-50-2": "Pontiac's plan at Detroit failed, his war went on for nearly three years, and at last he made peace.",
 "tcoo-69-1": "James Madison became President; the Shawnee leader Tecumseh worked to unite many nations to keep their land, and his brother the Prophet's warriors were defeated at Tippecanoe.",
 "tcoo-81-1": "James Buchanan became President, Minnesota and Oregon joined the Union, and the Latter-day Saints moved west to Utah, where they and the government came into conflict.",
 "tcoo-92-1": "After Lincoln's death Andrew Johnson became President; he fought with Congress over Reconstruction and was impeached but not removed, and the country bought Alaska from Russia.",
}

# Next shelf card (Omega Home Library shared engine). Only bots with a live link are shown to owners.
NEXT_SHELF = [
 {"name": "100 Years Ago Today", "shelf": "Scholar Shelf", "link": "https://x.ai/bot/5QXnAseS4QUrUnawaXEei",
  "why": "A real newspaper front page from 100 years ago each morning, family mode for ages 8 and up.",
  "when": "around ages 11 to 12, or when Story of America is finished"},
 {"name": "Founders' Reading Plan", "shelf": "Scholar Shelf", "link": "https://x.ai/bot/OiJ2yft0AxrfrCdRAgFYu",
  "why": "America's founding texts, about fifteen minutes a day, for older readers and grown-ups.",
  "when": "around ages 11 to 12, or when Story of America is finished"},
]

# Standards: code text checked word for word against the official documents (scripts/check_standards.py).
CCSS_SRC = "https://www.cde.ca.gov/be/st/ss/documents/finalelaccssstandards.pdf"
C3_SRC = "https://www.socialstudies.org/sites/default/files/c3/c3-framework-for-social-studies-rev0617.pdf"
STANDARDS = {
 "SL.2.2": {"framework": "CCSS-ELA", "band": "2", "source": CCSS_SRC, "printed_page": 27,
            "text": "Recount or describe key ideas or details from a text read aloud or information presented orally or through other media."},
 "RI.3.3": {"framework": "CCSS-ELA", "band": "3", "source": CCSS_SRC, "printed_page": 15,
            "text": "Describe the relationship between a series of historical events, scientific ideas or concepts, or steps in technical procedures in a text, using language that pertains to time, sequence, and cause/effect."},
 "RL.2.2": {"framework": "CCSS-ELA", "band": "2", "source": CCSS_SRC, "printed_page": 11,
            "text": "Recount stories, including fables and folktales from diverse cultures, and determine their central message, lesson, or moral."},
 "D2.His.1.3-5": {"framework": "C3", "band": "3-5", "source": C3_SRC, "printed_page": 46,
            "text": "Create and use a chronological sequence of related events to compare developments that happened at the same time."},
 "D2.His.4.3-5": {"framework": "C3", "band": "3-5", "source": C3_SRC, "printed_page": 47,
            "text": "Explain why individuals and groups during the same historical period differed in their perspectives."},
}
ACTIVITIES = {
 "tellBack": "Talk it over: the retell question after every reading",
 "whyQuestion": "Ages 9 to 12: the why question about how tonight's events connect",
 "timeline": "Library Card timeline entry when a chapter is finished, with same-time events side by side",
 "perspective": "Grown-up note plus a question about how another group at the time saw these events",
 "lesson": "Famous Stories: the question about the story's lesson",
}
VERIFIED = "2026-11-24"

# Display titles where the transcription's chapter heading differs from the 1917 printing.
# Reading text is never changed; the original heading is kept in chapters[].source_heading.
TITLE_FIXES = {
 51: ("The Boston Tea-Party", "The 1917 Doran printing reads THE BOSTON TEA-PARTY at the chapter head and "
      "The Boston Tea-Party in its contents; the transcription's heading reads The Boston Tea party."),
}
