DESIGN_SKILLS = set([
    # UI/UX & Product Design
    "ui", "ux", "ui/ux", "user interface", "user experience", "product design", "wireframing", "prototyping", 
    "user research", "usability testing", "interaction design", "ixd", "information architecture", "ia",
    "user journeys", "user flows", "personas", "storyboarding", "heuristic evaluation", "a/b testing",
    "accessibility", "wcag", "inclusive design", "design systems", "atomic design", "responsive design",
    "mobile design", "web design", "app design", "human-computer interaction", "hci", "user-centered design", "ucd",
    "service design", "experience design", "cx", "customer experience", "visual design", "ui components",
    "mockups", "high-fidelity", "low-fidelity", "affinity mapping", "card sorting", "tree testing",
    "contextual inquiry", "ethnographic research", "user interviews", "survey design", "data visualization",
    "microinteractions", "design thinking", "lean ux", "agile design", "design sprints", "rapid prototyping",

    # Graphic & Visual Design
    "graphic design", "branding", "identity design", "logo design", "typography", "color theory", "layout",
    "composition", "illustration", "vector graphics", "raster graphics", "print design", "packaging design",
    "poster design", "editorial design", "book design", "magazine design", "brochure design", "stationery design",
    "merchandise design", "infographics", "iconography", "pattern design", "surface design", "type design",
    "lettering", "calligraphy", "digital painting", "photo manipulation", "retouching", "color correction",
    "pre-press", "cmyk", "rgb", "pantone", "grid systems", "white space", "visual hierarchy",

    # Motion Graphics & Animation
    "motion graphics", "animation", "2d animation", "3d animation", "character animation", "storyboarding for motion",
    "keyframing", "easing", "rigging", "compositing", "vfx", "visual effects", "kinetic typography",
    "stop motion", "cel animation", "motion tracking", "particle systems", "rendering", "texturing",
    "lighting", "modeling", "3d modeling", "sculpting", "uv mapping", "materials", "shaders",

    # Software & Tools
    "figma", "sketch", "adobe xd", "invision", "framer", "marvel", "balsamiq", "zeplin", "abstract", "axure",
    "principle", "origami studio", "protopie", "adobe creative cloud", "photoshop", "illustrator", "indesign",
    "after effects", "premiere pro", "lightroom", "animate", "audition", "blender", "cinema 4d", "maya",
    "3ds max", "zbrush", "houdini", "unreal engine", "unity", "coreldraw", "affinity designer", "affinity photo",
    "affinity publisher", "procreate", "clip studio paint", "canva", "webflow", "wix", "squarespace",
    "spline", "vectary", "miro", "mural", "lucidchart", "whimsical", "optimal workshop",
    "maze", "hotjar", "crazy egg", "google analytics", "mixpanel", "amplitude", "notion", "airtable",

    # Web & Front-end (Designers often need some familiarity)
    "html", "html5", "css", "css3", "javascript", "js", "react", "vue", "angular", "tailwind", "sass", "less",
    "bootstrap", "material design", "apple human interface guidelines", "hig", "seo", "cms", "wordpress",
    "shopify", "e-commerce design", "landing page design", "email design", "newsletter design",

    # Architecture & Interior Design
    "architecture", "interior design", "spatial design", "environmental design", "exhibition design",
    "retail design", "wayfinding", "signage design", "cad", "autocad", "revit", "sketchup", "rhino",
    "grasshopper", "v-ray", "lumion", "enscape", "3d rendering", "drafting", "floor plans", "elevations",
    "sections", "building codes", "sustainable design", "leed", "materials selection", "furniture design",

    # Fashion & Textile Design
    "fashion design", "textile design", "apparel design", "pattern making", "draping", "sewing", "garment construction",
    "tech packs", "trend forecasting", "fabric sourcing", "knitwear", "menswear", "womenswear", "childrenswear",
    "accessories design", "footwear design", "jewelry design", "clo3d", "marvelous designer",

    # Game Design
    "game design", "level design", "character design", "environment design", "concept art", "ui/ux for games",
    "game mechanics", "storytelling", "narrative design", "world building", "playtesting", "game engine",

    # Industrial & Product Design (Physical)
    "industrial design", "product design (physical)", "cad modeling", "solidworks", "fusion 360", "inventor",
    "rapid prototyping", "3d printing", "cnc machining", "injection molding", "materials science",
    "ergonomics", "human factors", "manufacturing processes", "dfm", "design for manufacturing",

    # Soft Skills & Processes
    "creativity", "problem solving", "critical thinking", "collaboration", "communication", "presentation skills",
    "empathy", "attention to detail", "time management", "project management", "client relations",
    "design critiques", "feedback processing", "iteration", "brainstorming", "ideation", "concept development",

    # Niche / Specific
    "ar/vr design", "xr design", "augmented reality", "virtual reality", "mixed reality", "voice ui", "vui",
    "conversational design", "sound design", "audio design", "generative design", "computational design",
    "creative coding", "processing", "p5.js", "touchdesigner", "resolume", "projection mapping",

    # More specific variations and tools
    "lottie", "bodymovin", "svg animation", "webgl", "three.js", "glsl", "node-based compositing",
    "nuke", "fusion", "da vinci resolve", "final cut pro", "avid media composer", "color grading",
    "typography design", "custom lettering", "sign painting", "graffiti", "street art", "mural design",
    "riso printing", "screen printing", "letterpress", "bookbinding", "paper craft", "origami",
    "clay modeling", "woodworking", "metalworking", "ceramics", "glassblowing", "leathercraft",
    "fashion illustration", "storyboard animatics", "character turnaround", "model sheets", "prop design",
    "vehicle design", "creature design", "matte painting", "photobashing", "3d coat", "substance painter",
    "substance designer", "marmoset toolbag", "keyshot", "octane render", "redshift", "arnold render",
    "corona render", "clo 3d", "optitex", "gerber accumark", "lectra",
    "user testing", "remote usability testing", "moderated testing", "unmoderated testing",
    "eye tracking", "click tracking", "scroll maps", "heat maps", "session recording",
    "diary studies", "focus groups", "field studies", "desirability studies", "preference testing",
    "accessibility auditing", "color contrast", "screen readers", "keyboard navigation",
    "cognitive load", "gestalt principles", "fitts' law", "hick's law", "jakob's law", "miller's law",
    "occam's razor", "pareto principle", "parkinson's law", "serial position effect", "tesler's law",
    "von restorff effect", "zeigarnik effect", "aesthetic-usability effect", "doherty threshold",

    # Expanding Web & Mobile
    "ios design", "android design", "material you", "fluent design", "watchos design", "tvos design",
    "cross-platform design", "progressive web apps", "pwa", "single page applications", "spa",
    "dashboard design", "saas design", "b2b design", "b2c design", "enterprise design",
    "fintech design", "healthtech design", "edtech design", "gamification", "onboarding design",
    "empty states", "error states", "success states", "loading states", "skeleton screens",

    # Expanding Branding & Marketing
    "brand strategy", "brand guidelines", "brand manual", "logo marks", "logotypes", "monograms",
    "mascots", "brand voice", "brand positioning", "market research", "competitor analysis",
    "swot analysis", "mood boards", "stylescapes", "brand identity systems", "corporate identity",
    "advertising design", "social media graphics", "banner ads", "outdoor advertising", "billboard design",
    "vehicle wrap design", "event collateral", "trade show booth design",

    # Expanding Print & Packaging
    "die lines", "spot color", "foil stamping", "embossing", "debossing", "uv coating",
    "varnish", "paper stocks", "binding techniques", "saddle stitching", "perfect binding",
    "spiral binding", "wire-o binding", "coptic binding", "packaging structural design",
    "sustainable packaging", "corrugated board", "folding cartons", "rigid boxes", "flexible packaging",
    "label design", "hang tags", "blister packs", "clamshells",

    # Expanding 3D & Animation
    "hard surface modeling", "organic modeling", "retopology", "baking textures", "pbr textures",
    "physically based rendering", "character rigging", "facial rigging", "blend shapes", "morph targets",
    "inverse kinematics", "forward kinematics", "motion capture", "mocap", "fluid simulation",
    "smoke simulation", "fire simulation", "cloth simulation", "hair/fur simulation", "rigid body dynamics",
    "soft body dynamics", "particle flow", "crowd simulation",

    # Expanding Tools
    "corel painter", "manga studio", "opentoonz", "tvpaint", "toon boom harmony", "moho", "spine 2d",
    "dragonframe", "cavalry", "natron", "blackmagic fusion", "silhouettefx", "mocha pro",
    "pf track", "syntheyes", "boujou", "zbrushcore", "mudbox", "3dcoat", "topogun", "rizomuv",
    "substance alchemist", "quixel mixer", "quixel megascans", "speedtree", "plantfactory",
    "terragen", "vue xstream", "world machine", "gaea", "clarisse ifx", "katana", "mari",

    # More specific UI/UX terms
    "omnichannel experience", "journey mapping", "mind mapping", "user stories", "use cases",
    "scenarios", "task analysis", "context of use", "cognitive walkthrough", "expert review",
    "summative evaluation", "formative evaluation", "benchmark testing", "first click testing",
    "five second test", "semantic differential", "system usability scale", "sus", "net promoter score",
    "nps", "customer satisfaction", "csat", "customer effort score", "ces", "kpis",
    "conversion rate optimization", "cro", "funnel analysis", "drop-off rate", "bounce rate",
    "time on task", "success rate", "error rate", "satisfaction metrics",

    # Business of Design
    "design strategy", "design leadership", "design management", "design ops", "design operations",
    "research ops", "agile methodology", "scrum framework", "kanban", "waterfall methodology",
    "budgeting", "estimating", "proposal writing", "pitching", "contract negotiation",
    "intellectual property", "copyright", "trademark", "patent", "nda", "non-disclosure agreement",
    "sow", "statement of work", "rfp", "request for proposal", "invoicing", "time tracking",

    # Even more random design related things
    "generative ai", "midjourney", "dall-e", "stable diffusion", "prompt engineering",
    "ai-assisted design", "algorithmic design", "parametric design", "vdm", "voxel design",
    "nurbs modeling", "subdivision surfaces", "boolean operations", "csg", "constructive solid geometry",
    "point cloud data", "photogrammetry", "lidar scanning", "3d scanning", "reverse engineering",
    "bionics", "biomimicry", "cradle to cradle", "circular economy", "life cycle assessment",
    "lca", "design for disassembly", "upcycling", "recycling", "sustainable materials",
    "smart materials", "nanomaterials", "shape memory alloys", "piezoelectric materials",
    "thermochromic materials", "photochromic materials", "electroluminescent materials",
    "e-textiles", "wearable technology", "smart clothing", "interactive textiles",

    # Adding a ton of variations to hit >500
    "visual communication", "information design", "data design", "diagramming",
    "concept generation", "visual exploration", "style frames", "moodboarding",
    "creative direction", "art direction", "design direction", "design concept",
    "visual language", "brand language", "design vocabulary", "visual system",
    "grid design", "layout design", "page design", "screen design", "interface design",
    "interaction logic", "state transitions", "animation curves", "motion principles",
    "squash and stretch", "anticipation", "staging", "straight ahead action and pose to pose",
    "follow through and overlapping action", "slow in and slow out", "arcs", "secondary action",
    "timing", "exaggeration", "solid drawing", "appeal",
    "color palettes", "color schemes", "monochromatic", "analogous", "complementary",
    "split-complementary", "triadic", "tetradic", "warm colors", "cool colors",
    "hue", "saturation", "lightness", "brightness", "value", "tint", "shade", "tone",
    "contrast", "alignment", "repetition", "proximity", "balance", "symmetry", "asymmetry",
    "tension", "rhythm", "scale", "proportion", "golden ratio", "rule of thirds",
    "fibonacci sequence", "gestalt", "figure-ground", "similarity", "closure", "continuity",
    "common fate", "good form", "past experience",
    "user modeling", "mental models", "conceptual models", "system models", "affordances",
    "signifiers", "mapping", "constraints", "feedback", "discoverability", "understandability",
    "slip", "mistake", "error prevention", "error recovery", "graceful degradation",
    "progressive enhancement", "mobile first", "desktop first", "content first",
    "content strategy", "copywriting", "ux writing", "microcopy", "tone of voice",
    "multilingual design", "localization", "internationalization", "i18n", "l10n",
    "rtl design", "ltr design", "bidi text", "typography hierarchy", "font pairings",
    "kerning", "tracking", "leading", "line height", "line length", "measure",
    "orphan", "widow", "rag", "justification", "hyphenation", "drop cap", "ligatures",
    "swashes", "small caps", "old style figures", "lining figures", "tabular figures",
    "proportional figures", "fractions", "superscript", "subscript", "glyphs", "diacritics"
])

