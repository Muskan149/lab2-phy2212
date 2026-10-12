GlowScript 3.0 VPython

## PHYS 2212 Online
## Lab 2: Lines of Charge
## Completed from 2212-lab2start.py
## ===================

## ===================
## PHYSICAL CONSTANTS
## ===================

oofpez = 9e9
g = 9.81


## =================================
## EDIT TO ADD YOUR OBSERVED VALUES
## =================================
## Values from my Lab 1 report:
##   Tape B (floating, top) length   = 19.2 cm
##   Tape A (bottom) length          = 20 cm
##   Tape width                      = 1.9 cm (standard 3/4 inch tape)
##   Mass per area                   = 1 g/m^2 = 1e-3 kg/m^2
##   Separation where B floats       d = 0.2 cm = 2e-3 m
##   Mass of B = (1e-3 kg/m^2)(0.192 m)(0.019 m) = 3.65e-6 kg

# Mass of one tape (in kg) -- EDIT THIS NEXT LINE
M = 1e-3 * 0.192 * 0.019    # = 3.65e-6 kg

# Estimated net charge on one tape (in C) -- EDIT THIS NEXT LINE
# Tuned until the electric force on TopTape balances its weight (F_E ~= M*g)
Q = 8.95e-10



## =================================================
## EDIT TO CREATE A FUNCTION FOR THE ELECTRIC FIELD
## (you can copy your work from Lab 0)
## =================================================

def Efield(chargedParticle,observationLocation):
    r = observationLocation - chargedParticle.pos     # from source to observation point
    E = oofpez * chargedParticle.charge / mag(r)**2 * norm(r)
    return(E)



## ========================================
## THIS FUNCTION CREATES A LINE OF CHARGE
##  v v v DO NOT ALTER THIS FUNCTION v v v
## ========================================

def lineCharge(startPos, axis, mass, charge, N, color=color.red):
    # Creates a line of N uniform point charges with a given total charge and
    # mass arranged at equal intervals on a line segment starting at startPos
    # and extending along axis
    line = []
    line.axis = axis
    line.pos = startPos
    spacing = axis/(N-1)   # vector separating adjacent charges
    q = Q/N     # magnitude of each point charge
    m = M/N     # mass of each point charge
    for ii in range(N):
        # There will be N point charges in this tape
        dq = sphere(pos=startPos+(ii*spacing), radius=mag(axis)/N, color=color)
        dq.charge = q
        dq.mass = m
        line.append(dq)
    return(line)

## ===============================================
##  ^ ^ ^  DO NOT ALTER THE ABOVE FUNCTION ^ ^ ^
## ===============================================



## ============================================================
## CREATING THE TAPES
## Each tape is modeled as N point charges side-by-side in a line.
## TopTape (tape B) floats d = 0.002 m above BottomTape (tape A), centered over it.
## ============================================================

d = 0.002      # float height in m (Lab 1)
L_top = 0.192  # length of floating tape B in m
L_bot = 0.20   # length of bottom tape A in m
N = 200        # charges per tape; spacing (~1 mm) must be small compared with d

TopTape = lineCharge(startPos=vector((L_bot-L_top)/2,d,0), axis=vector(L_top,0,0), mass=M, charge=Q, N=N, color=color.red)
BottomTape = lineCharge(startPos=vector(0,0,0), axis=vector(L_bot,0,0), mass=M, charge=Q, N=N, color=color.blue)



## ============================================================
## CALCULATING THE ELECTRIC FIELD AND THE ELECTRIC FORCE
## (E at the location of TopTape produced by BottomTape, and F_E on TopTape due to BottomTape)
## ============================================================

E_scale = 2.5e-7  # arrowscale for electric field vector arrows

F_E_on_top = vector(0,0,0)   # net electric force on TopTape initialized at zero
F_E_scale = 800              # arrowscale for electric force arrow
F_G_scale = F_E_scale        # arrowscale for gravity force arrow

for dq_top in TopTape:   # iterate through each piece of charge in TopTape
    E_at_dq_top = vector(0,0,0)   # initializing the net electric field at dq_top
    E_at_dq_top_arrow = arrow(pos=dq_top.pos, axis=E_scale*E_at_dq_top, color=color.green)

    for dq_bottom in BottomTape:   # iterate through each piece of charge in BottomTape
        # Calculate E-field at the location of dq_top due to dq_bottom
        dE_at_dq_top_by_dq_bottom = Efield(dq_bottom, dq_top.pos)
        E_at_dq_top = E_at_dq_top + dE_at_dq_top_by_dq_bottom

        # Calculate the electric force on dq_top due to dq_bottom
        F_E_on_dq_top_by_dq_bottom = dq_top.charge * dE_at_dq_top_by_dq_bottom
        F_E_on_top = F_E_on_top + F_E_on_dq_top_by_dq_bottom

    # Arrow for the net electric field at dq_top due to BottomTape
    E_at_dq_top_arrow.axis = E_scale*E_at_dq_top



## ============================================================
## NET ELECTRIC FORCE AND GRAVITATIONAL FORCE
## ============================================================

middleTop = TopTape.pos + 0.5*TopTape.axis   # tails of the arrows in the middle of TopTape

# Electric force vector
F_E_arrow = arrow(pos=middleTop, axis=F_E_scale*F_E_on_top, color=color.white)

# Gravitational force vector
F_grav = vector(0, -M*g, 0)
F_G_arrow = arrow(pos=middleTop, axis=F_G_scale*F_grav, color=color.yellow)

print("Magnitude of electric force:", mag(F_E_on_top))
print("Magnitude of gravitational force:", M*g)
print("Ratio F_E / F_G:", mag(F_E_on_top)/(M*g))

# Because F_E scales as Q^2, this is the charge that would balance gravity exactly:
print("Charge per tape that balances gravity (C):", Q*sqrt(M*g/mag(F_E_on_top)))

# Point-charge comparison (Lab 1 model): all charge at each tape's center
Q_point = sqrt(M*g*d**2/oofpez)
print("Point-charge model estimate (C):", Q_point)
print("All done!")
