import os
import subprocess

def get_full_theory(theory, laws):
    return fr"""
        r1 : right(directive, Art, Right, Option, Facts), prolog(member(Y, {laws})), right(Y, Art1, Right, Option, Facts) -> conformity(Y, Art).
        r2 : right(directive, Art, Right, Option, Facts), prolog(member(Y, {laws})), right(Y, Art1, Right, Option, Facts1), prolog(Facts \= Facts1) => partialConformity(Y, Art).
        r3 : right(directive, Art, Right, Option, Facts), prolog(member(Y, {laws})), ~(right(Y, Art, Right, Option, Facts)) -> -conformity(Y, Art).
        conflict([conformity(Y, Art)], [partialConformity(Y, Art)]).
    """ + "\n\n" + theory

def run_reasoner(theory):
    reasoner = os.path.join(os.path.abspath(os.path.dirname(__file__)), "arg2p_grounded_no_pref_repl.jar")
    try:
        return subprocess.run(
            ["java", "-jar", reasoner, theory],
            capture_output=True,
            text=True,
            check=True
        ).stdout
    except subprocess.CalledProcessError as e:
        print(e)
        return ""

if __name__ == "__main__":
    theory = get_full_theory("""
        f1 :-> right(directive, x, y, z, [a, b, c]).
        f2 :=> right(es, x, y, z, [a]).
        f3 :=> right(es, x, y, z, [a, b, c]).
    """, ["es"])

    print(run_reasoner(theory))
