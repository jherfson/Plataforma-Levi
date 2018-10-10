from pymatgen import MPRester, Element
from pymatgen.analysis.phase_diagram import GrandPotentialPhaseDiagram, \
    PhaseDiagram, PDPlotter
import mu_to_T


def plot_pd(pd, show_unstable=False):
    plotter = PDPlotter(pd, show_unstable=0.03)
    plotter.show()
    # plotter.write_image("{}.png".format('-'.join(system)), "png")  # save figure


def analyze_pd(pd):
    print('Stable Entries (formula, materials_id)\n--------')
    for e in pd.stable_entries:
        print(e.composition.reduced_formula, e.entry_id)

    print('\nUnstable Entries (formula, materials_id, e_above_hull (eV/atom), decomposes_to)\n--------')
    for e in pd.unstable_entries:
        decomp, e_above_hull = pd.get_decomp_and_e_above_hull(e)
        pretty_decomp = [("{}:{}".format(k.composition.reduced_formula, k.entry_id), round(v, 2)) for k, v in decomp.items()]
        print(e.composition.reduced_formula, e.entry_id, "%.3f" % e_above_hull, pretty_decomp)

if __name__ == "__main__":
    MAPI_KEY = "key"  # You must change this to your Materials API key! (or set MAPI_KEY env variable)
    system = ["La", "Ni","Mn", "O"]  # system we want to get open PD for
    # system = ["Li", "Fe", "P", "O"]  # alternate system example

    open_elements_specific = None  # e.g., {Element("O"): 0} where 0 is the specific chemical potential
    open_element_all = Element("O")  # plot a series of open phase diagrams at critical chem pots with this element open

    mpr = MPRester(MAPI_KEY)  # object for connecting to MP Rest interface

    # get data
    entries = mpr.get_entries_in_chemsys(system, compatible_only=True)

    if open_elements_specific:
        gcpd = GrandPotentialPhaseDiagram(entries, open_elements_specific)
        plot_pd(gcpd, False)
        analyze_pd(gcpd)

    if open_element_all:
        pd = PhaseDiagram(entries)
        chempots = pd.get_transition_chempots(open_element_all)
        all_gcpds = list()
        for idx in range(len(chempots)):
            if idx == len(chempots) - 1:
                avgchempot = chempots[idx] - 0.1
            else:
                avgchempot = 0.5 * (chempots[idx] + chempots[idx + 1])
            gcpd = GrandPotentialPhaseDiagram(entries, {open_element_all: avgchempot}, pd.elements)
            min_chempot = None if idx == len(chempots) - 1 else chempots[idx + 1]
            max_chempot = chempots[idx]
            print("Chempot range for diagram {} is: {} to {}".format(idx, min_chempot, max_chempot))
            mu_to_T.print_T_corresponding_to_mu_equals(max_chempot)
            mu_to_T.print_T_corresponding_to_mu_equals(min_chempot)
            plot_pd(gcpd, False)
