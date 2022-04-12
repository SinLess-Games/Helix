package com.sinlessgamesllc.service;

import com.sinlessgamesllc.domain.Deals;
import com.sinlessgamesllc.repository.DealsRepository;
import java.util.List;
import java.util.Optional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Service Implementation for managing {@link Deals}.
 */
@Service
@Transactional
public class DealsService {

    private final Logger log = LoggerFactory.getLogger(DealsService.class);

    private final DealsRepository dealsRepository;

    public DealsService(DealsRepository dealsRepository) {
        this.dealsRepository = dealsRepository;
    }

    /**
     * Save a deals.
     *
     * @param deals the entity to save.
     * @return the persisted entity.
     */
    public Deals save(Deals deals) {
        log.debug("Request to save Deals : {}", deals);
        return dealsRepository.save(deals);
    }

    /**
     * Partially update a deals.
     *
     * @param deals the entity to update partially.
     * @return the persisted entity.
     */
    public Optional<Deals> partialUpdate(Deals deals) {
        log.debug("Request to partially update Deals : {}", deals);

        return dealsRepository
            .findById(deals.getId())
            .map(existingDeals -> {
                if (deals.getName() != null) {
                    existingDeals.setName(deals.getName());
                }
                if (deals.getPrice() != null) {
                    existingDeals.setPrice(deals.getPrice());
                }
                if (deals.getDescription() != null) {
                    existingDeals.setDescription(deals.getDescription());
                }
                if (deals.getImage() != null) {
                    existingDeals.setImage(deals.getImage());
                }
                if (deals.getImageContentType() != null) {
                    existingDeals.setImageContentType(deals.getImageContentType());
                }

                return existingDeals;
            })
            .map(dealsRepository::save);
    }

    /**
     * Get all the deals.
     *
     * @return the list of entities.
     */
    @Transactional(readOnly = true)
    public List<Deals> findAll() {
        log.debug("Request to get all Deals");
        return dealsRepository.findAll();
    }

    /**
     * Get one deals by id.
     *
     * @param id the id of the entity.
     * @return the entity.
     */
    @Transactional(readOnly = true)
    public Optional<Deals> findOne(Long id) {
        log.debug("Request to get Deals : {}", id);
        return dealsRepository.findById(id);
    }

    /**
     * Delete the deals by id.
     *
     * @param id the id of the entity.
     */
    public void delete(Long id) {
        log.debug("Request to delete Deals : {}", id);
        dealsRepository.deleteById(id);
    }
}
