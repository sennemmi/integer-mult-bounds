from pathlib import Path
from collections import Counter
from math import exp,log
import sys,json,types,time,importlib.util,hashlib
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
R=Path(__file__).resolve().parents[2]; PKG=R/'research/paired-cube-diagonal-bit-168'; BIT=PKG/'bit'; OUT=R/'research/paired-cube-diagonal-bit-168-followup'
sys.path.insert(0,str(BIT));sys.path.insert(0,str(PKG/'arithmetic'))
try:import resource
except ImportError:sys.modules['resource']=types.ModuleType('resource')
from word import Candidate
from prove import certify
w=Candidate();w.exact_frames();C=w.C;h=w.h
base_row=w.row();cert=json.loads((PKG/'certificate.json').read_text())['bit'];baseprof=cert['profile'];hist={int(k):v for k,v in baseprof['child_histogram'].items()};m=baseprof['m'];W=baseprof['W_per_vertex']
selection=json.loads((PKG/'selected/bit/sinks.json').read_text());sink_roles={w.w['rootroles'][x['root']] for x in selection}
sink_ops={i for s in sink_roles for i in w.role_ops[s]}
# Construct the exact physical register chains used by Candidate.row(), including donor/gauge splices.
role_entries={s:[] for s in range(w.R)}
for i in w.phase1+w.rest:
    a,b,_=w.ops[i]
    role_entries[a].append(('op',i));role_entries[b].append(('op',i))
for j,s in enumerate(w.w['rootroles']):role_entries[s].append(('frame',w.w['root_frame'][j]))
start={s:w.w['source_frame'][n] for n,s in w.source.items()};start.update({s:z['frame'] for s,z in w.gauge.items()})
recipient={d:b for b,d in w.pairs}
physical_chains=[];op_info={i:[] for i in range(len(w.ops))}
for rep in range(w.R):
    if rep in w.donor:continue
    entries=list(role_entries[rep])
    if rep in recipient:
        b=recipient[rep];entries.append(('frame',w.gauge[b]['frame']));entries.extend(role_entries[b])
    entries.append(('frame',w.w['full_frame']))
    prev=start.get(rep)
    chain=[]
    for kind,value in entries:
        frame=w.opframe[value] if kind=='op' else value
        chain.append((kind,value,frame,prev))
        prev=frame
    for j,(kind,value,frame,prev) in enumerate(chain):
        if kind!='op':continue
        nextf=chain[j+1][2]
        op_info[value].append((prev,nextf,rep))
    physical_chains.append(chain)
assert all(len(op_info[i])==2 for i in range(len(w.ops)))
def sub_basis(B,f):return len(B)<=C.dimf[f] and all(w.module.dot(a,b)==0 for a in C.A[f] for b in B)
def moment_float(H,a):
    count=sum(H.values());z=0.0
    for t,n in H.items():z+=(t*n/(m*W))*exp(a*log(m/t))
    return z+1e-16*(32*m*count/W)*exp(a*log(m))
def root_float(H):
    lo,hi=0.0,0.01
    for _ in range(60):
        mid=(lo+hi)/2
        if moment_float(H,mid)<1:lo=mid
        else:hi=mid
    return (lo+hi)/2
base_root=root_float(hist);existing={tuple(sorted(map(tuple,B),key=lambda r:next(j for j,x in enumerate(r) if x))):f for f,B in C.B.items()}
valid=[];lowerings=Counter();structural=0
for i,(a,b,n) in enumerate(w.ops):
    ports=op_info[i]
    if i in sink_ops:continue
    rows=[]
    for pf,nf,rep in ports:
        if pf is not None:rows.extend(C.B[pf])
    bits=C.sup[n]
    while bits:
        low=bits&-bits;bits-=low;rows.append(C.chi[low.bit_length()-1])
    B,_=w.module.reduce_rows(rows,h);B=tuple(sorted(map(tuple,B),key=lambda r:next(j for j,x in enumerate(r) if x)))
    old=w.opframe[i];olddim=C.dimf[old];d=len(B)
    if d>=olddim:continue
    lowerings[olddim-d]+=1
    if not all(sub_basis(B,nf) for pf,nf,rep in ports):continue
    structural+=1
    f=existing.get(B)
    if f is None:f=w.register(B)
    if not C.nondeg(f) or not all(C.sub(pf,f) for pf,nf,rep in ports if pf is not None):continue
    delta=Counter()
    for pf,nf,rep in ports:
        p=0 if pf is None else C.dimf[pf];q=C.dimf[nf];newd=C.dimf[f]
        for x,sign in ((olddim,-1),(newd,1)):
            if x>p:delta[x-p]+=sign
            if q>x:delta[q-x]+=sign
    H=Counter(hist)
    for r,k in delta.items():H[r]+=3*k
    H={r:v for r,v in H.items() if v}
    if any(v<0 for v in H.values()):continue
    gain=root_float(H)-base_root
    if gain>0:valid.append(dict(score=gain,i=i,old=old,new=f,olddim=olddim,newdim=C.dimf[f],delta=dict(delta)))
byop={x['i']:x for x in valid};conflict={i:set() for i in byop}
for chain in physical_chains:
    ops=[value for j,(kind,value,frame,prev) in enumerate(chain) if kind=='op']
    for i,j in zip(ops,ops[1:]):
        if i in byop and j in byop:conflict[i].add(j);conflict[j].add(i)
chosen=set()
for x in sorted(valid,key=lambda z:(-z['score'],z['i'])):
    if not(conflict[x['i']]&chosen):chosen.add(x['i'])
# Strict one-for-neighbor improvement on the deterministic greedy independent set.
changed=True
while changed:
    changed=False
    for x in sorted((z for z in valid if z['i'] not in chosen),key=lambda z:(-z['score'],z['i'])):
        neigh=conflict[x['i']]&chosen
        if x['score']>sum(byop[j]['score'] for j in neigh)+1e-15:
            chosen.difference_update(neigh);chosen.add(x['i']);changed=True
selected=[byop[i] for i in sorted(chosen)]
old_internal={int(k):v for k,v in base_row['physical_internal_histogram'].items()}
for x in selected:w.opframe[x['i']]=x['new']
w.changed_frames=[i for i,(a,b) in enumerate(zip(w.original_opframe,w.opframe)) if a!=b];w.w['op_frame']=w.opframe[:]
w.exact_frames();after_row=w.row()
actual_delta=Counter({int(k):v for k,v in after_row['physical_internal_histogram'].items()});actual_delta.subtract(old_internal);actual_delta=Counter({r:n for r,n in actual_delta.items() if n})
pred=Counter()
for x in selected:pred.update(x['delta'])
pred=Counter({r:n for r,n in pred.items() if n})
assert actual_delta==pred,(actual_delta,pred)
newhist=Counter(hist)
for r,n in actual_delta.items():newhist[r]+=3*n
newhist={r:n for r,n in newhist.items() if n};assert all(n>0 for n in newhist.values())
profile=dict(baseprof);profile['child_histogram']=newhist;profile['rank_per_vertex']=sum(r*n for r,n in newhist.items());profile['maxchild']=max(newhist)
profile['changed_operation_frames']=after_row['changed_operation_frames'];profile['frames_not_contained_in_original']=after_row['frames_not_contained_in_original']
physical={int(k):v for k,v in baseprof['physical_internal_histogram'].items()}
for r,n in actual_delta.items():physical[r]=physical.get(r,0)+n
profile['physical_internal_histogram']={r:n for r,n in physical.items() if n}
exact=certify(profile)
AP=R/'research/source-assisted/global/assemble_profiles.py';spec=importlib.util.spec_from_file_location('pr184_assembly',AP);pr=importlib.util.module_from_spec(spec);spec.loader.exec_module(pr)
old_bit=pr.select(pr.normalize(baseprof),True);new_bit=pr.select(pr.normalize(profile),True)
leafspec=importlib.util.spec_from_file_location('v4_assembly',R/'research/source-assisted-v4/assemble.py');leafmod=importlib.util.module_from_spec(leafspec);leafspec.loader.exec_module(leafmod)
old_bit,_=leafmod.bootstrap_bit_leaf(old_bit);new_bit,new_bootstrap=leafmod.bootstrap_bit_leaf(new_bit)
sa=json.loads((R/'research/source-assisted-v4/certificate.json').read_text());complex_price=pr.select(pr.normalize(sa['complex_profile']))
complex_profile_sha256=hashlib.sha256(json.dumps(sa['complex_profile'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
base_assembled=pr.assemble(complex_price,old_bit,R,R/'research/source-assisted/global/FINITE_BRIDGE.txt')
assembled=pr.assemble(complex_price,new_bit,R,R/'research/source-assisted/global/FINITE_BRIDGE.txt')
# Keep only selected physical frames; each ID is reproducible from the frozen source frame table plus append order.
initial_ids={int(k) for k in w.C.fr['frames']}
frame_records={str(f):[list(r) for r in C.B[f]] for f in sorted({x['new'] for x in selected}) if f not in initial_ids}
plan=dict(search='single-operation endpoint lower-frame descent; floating scores rank proposals, exact physical and rational checks certify the accepted batch; deterministic greedy independent set on consecutive physical-chain conflicts',seed=None,
 baseline_head='a1175449f34d39ff933d9d8ab23ced1f32b290ec',terminal_sink_count=len(selection),screened_dimension_lowerings=dict(sorted(lowerings.items())),
 structural_candidates=structural,positive_candidates=len(valid),selected_count=len(selected),selected_operations=[dict(operation=x['i'],old_frame=x['old'],new_frame=x['new'],old_dimension=x['olddim'],new_dimension=x['newdim'],rank_delta=x['delta']) for x in selected],
 new_frame_records=frame_records,physical_internal_delta=dict(sorted(actual_delta.items())),baseline_bit_coarse=str(certify(baseprof)['coarse_saving']),candidate_bit_coarse=str(exact['coarse_saving']),
 baseline_bit_effective=str(old_bit['effective_saving']),candidate_bit_effective=str(new_bit['effective_saving']),baseline_kappa=str(base_assembled['kappa']),candidate_kappa=str(assembled['kappa']),
 selected_coarse_saving=str(new_bit['saving']),candidate_initial_effective_saving=new_bootstrap['input_effective_saving'],finite_leaf_savings=new_bootstrap['finite_leaf_savings'],
 complex_profile_sha256=complex_profile_sha256,
 checks=dict(exact_frame_geometry=True,full_physical_role_chain_row=True,exact_rank_histogram=True,exact_paid_moment=True,selected_terminal_ops_unchanged=True))
plan['plan_sha256']=hashlib.sha256(json.dumps(plan,sort_keys=True,separators=(',',':')).encode()).hexdigest()
planpath=OUT/'frame-descent.json';planpath.write_text(json.dumps(plan,indent=2,sort_keys=True)+'\n')
from fractions import Fraction
print(json.dumps(dict(ops=len(w.ops),physical_chains=len(physical_chains),lowerings=dict(sorted(lowerings.items())),structural=structural,positive=len(valid),selected=len(selected),
 changed_operation_frames=after_row['changed_operation_frames'],dimension_gain=sum(x['olddim']-x['newdim'] for x in selected),physical_internal_delta=dict(sorted(actual_delta.items())),
 bit_coarse_before=str(certify(baseprof)['coarse_saving']),bit_coarse_after=str(exact['coarse_saving']),bit_effective_before=str(old_bit['effective_saving']),bit_effective_after=str(new_bit['effective_saving']),
 kappa_before=str(base_assembled['kappa']),kappa_after=str(assembled['kappa']),gain=str(assembled['kappa']-Fraction(base_assembled['kappa'])),plan=str(planpath)),sort_keys=True),flush=True)
