// ====================================================================================
// GUNDAM ROBOTICS SYSTEMS & UNIVERSITY OF WASHINGTON DEPARTMENT OF PHYSICS
// Subsystem: master_ema_assembly.scad (MDOF Power-by-Wire Actuator Core)
// Core Source: github.com/Gundam-Robotics-Systems/Electromagnetic-Actuator
// Architecture: 48V-5A Base Architecture with Integrated Fused Silica Liners
// Center Origin (0,0,0) = Concentric Centerpoint of the Piston Shaft Neutral Axis
// ====================================================================================

$fn = 100; // High-fidelity CNC milling and coil winding clearance path resolution

// --- Gundam Robotics EMA Physical Constants (mm) ---
casing_outer_dia   = 110.00;             // Outer magnetic containment shell cylinder
casing_total_len   = 320.00;             // Total longitudinal actuator body envelope
fused_silica_dia   = 76.20;              // High-dielectric fused silica isolation sleeve
piston_rod_dia     = 35.00;              // Central dual-motion (axial/rotational) piston rod
bitter_coil_pitch  = 18.00;              // Step interval for multi-phase magnetic fields

module fused_silica_liner() {
    echo("EXTRUDING GUNDAM ROBOTICS ENCLOSURE LINER: FUSED SILICA HIGH-DIELECTRIC BARRIER");
    color("LightBlue", 0.4) { // Transparent insulation sleeve representation
        difference() {
            cylinder(d=fused_silica_dia, h=casing_total_len - 10, center=true);
            cylinder(d=fused_silica_dia - 8, h=casing_total_len + 2, center=true);
        }
    }
}

module bitter_coil_layers() {
    echo("STAMPING MULTI-PHASE HELICAL BITTER COIL MATRIX (48V-5A DRIVE PROFILE)");
    // Helical overlapping coil slots that drive simultaneous linear push and torque rotation
    color("Copper") {
        for (z_step = [-casing_total_len/2 + 30 : bitter_coil_pitch : casing_total_len/2 - 30]) {
            translate([0, 0, z_step])
                rotate([12.5, 0, 0]) // Mandatory 12.5° helical twist pattern for dual-motion torque
                    difference() {
                        cylinder(d=casing_outer_dia - 12, h=10, center=true);
                        cylinder(d=fused_silica_dia + 2, h=12, center=true);
                    }
        }
    }
}

module dual_motion_piston_shaft() {
    echo("MACHINING CENTRAL DIRECT-DRIVE CHROME PISTON ROD");
    // Moves back and forth (linear) and twists (rotational) natively via the Lorentz Ejection rule
    color("Chrome") {
        translate([0, 0, 20]) { // Shown with a 20mm active linear stroke displacement
            rotate([0, 0, 45]) { // Shown with a 45° active rotational torque indexing displacement
                difference() {
                    cylinder(d=piston_rod_dia, h=casing_total_len + 120, center=true);
                    // Internal core cavity reducing unsprung kinetic mass boundaries
                    cylinder(d=piston_rod_dia - 10, h=casing_total_len + 124, center=true);
                }
            }
        }
    }
}

// --- Composite Electromagnetic Actuator Instantiation ---
union() {
    fused_silica_liner();
    bitter_coil_layers();
    dual_motion_piston_shaft();
    
    // Outer Armor Shield Housing
    color("DarkSlateGrey", 0.7) {
        difference() {
            cylinder(d=casing_outer_dia, h=casing_total_len, center=true);
            cylinder(d=casing_outer_dia - 8, h=casing_total_len + 4, center=true);
        }
    }
}
