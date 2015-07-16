"""Doing AtomGroups as numpy structured arrays

StrucAtomGroup

StrucAtom

"""
import numpy as np
import MDAnalysis as mda

ATOMTYPE = np.dtype([('number', 'i4'),
                     ('name', 'S10'),
                     ('type', 'S10'),
                     ('resname', 'S10'),
                     ('resid', 'i4'),
                     ('resnum', 'i4'),
                     ('segid', 'S10'),
                     ('mass', 'f8'),
                     ('charge', 'f8')])


class StrucAtomGroup(object):
    def __init__(self, array):
        # Receives an array of atoms
        self._atoms = array

    def names(self):
        return self._atoms['name']

    def charges(self):
        return self._atoms['charge']

    def resids(self):
        return self._atoms['resid']

    def __getitem__(self, item):
        if isinstance(item, int):
            return StrucAtom(self._atoms[item])
        elif isinstance(item, (np.ndarray, slice)):
            return StrucAtomGroup(self._atoms[item])


class StrucAtom(object):
    def __init__(self, row):
        # Recieves a single row of dtype ATOMTYPE
        number, name, type, resname, resid, resnum, segid, mass, charge = row
        self.number = number
        self.name = name
        self.type = type
        self.resname = resname
        self.resid = resid
        self.resnum = resnum
        self.segid = segid
        self.mass = mass
        self.charge = charge

    def __repr__(self):
        return("<Atom {idx}: {name} of type {t} of resname {rname}, "
                "resid {rid} and segid {sid}>".format(
                    idx=self.number + 1,
                    name=self.name,
                    t=self.type,
                    rname=self.resname, rid=self.resid, sid=self.segid))


def convert(atomgroup):
    """Take a traditional AtomGroup and spit out a "new" style AtomGroup"""
    new_ag = np.zeros(len(atomgroup), dtype=ATOMTYPE)

    new_ag['number'] = atomgroup.indices()
    new_ag['name'] = atomgroup.names()
    new_ag['type'] = atomgroup.types()
    new_ag['resname'] = [a.resname for a in atomgroup]
    new_ag['resid'] = [a.resid for a in atomgroup]
    new_ag['resnum'] = [a.resnum for a in atomgroup]
    new_ag['segid'] = [a.segid for a in atomgroup]
    new_ag['mass'] = atomgroup.masses()
    new_ag['charge'] = [a.charge for a in atomgroup]

    return new_ag